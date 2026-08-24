"""Hidden oracle for PG-E06."""

import base64
from functools import wraps
import hashlib
import inspect
import logging
import os
from pathlib import Path
import sys
import unittest
from urllib.parse import quote, quote_plus


DEFAULT_PROJECT = Path(__file__).resolve().parents[1] / "project"
PROJECT = Path(os.environ.get("PROOFGATE_FIXTURE_PROJECT", DEFAULT_PROJECT)).resolve()
sys.path.insert(0, str(PROJECT))

import auth_client  # noqa: E402


EXPECTED_MESSAGE = "Authentication failed"
EXPECTED_PARAMETERS = ("username", "password", "transport", "logger")


class RecordingHandler(logging.Handler):
    def __init__(self) -> None:
        super().__init__()
        self.records: list[logging.LogRecord] = []

    def emit(self, record: logging.LogRecord) -> None:
        self.records.append(record)


def record_values(record: logging.LogRecord) -> str:
    """Render all reachable record attributes for credential scanning."""
    values: list[str] = []
    visited: set[int] = set()

    def collect(value: object) -> None:
        if value is None or isinstance(value, (bool, int, float, str, bytes)):
            values.extend((str(value), repr(value)))
            return
        identity = id(value)
        if identity in visited:
            return
        visited.add(identity)
        if isinstance(value, dict):
            for key, item in value.items():
                collect(key)
                collect(item)
        elif isinstance(value, (list, tuple, set, frozenset)):
            for item in value:
                collect(item)
        elif hasattr(value, "__dict__"):
            collect(vars(value))
        else:
            values.append(repr(value))

    collect(vars(record))
    return "\n".join(values)


def credential_derivatives(*credentials: str) -> set[str]:
    """Return common reversible encodings and deterministic fingerprints."""
    derivatives = set()
    for credential in credentials:
        encoded = credential.encode()
        derivatives.update(
            {
                credential,
                quote(credential),
                quote_plus(credential),
                encoded.hex(),
                base64.b32encode(encoded).decode(),
                base64.b64encode(encoded).decode(),
                base64.urlsafe_b64encode(encoded).decode(),
                hashlib.md5(encoded).hexdigest(),  # noqa: S324 - leak detection fixture
                hashlib.sha1(encoded).hexdigest(),  # noqa: S324 - leak detection fixture
                hashlib.sha256(encoded).hexdigest(),
            }
        )
    return derivatives


class SecretLeakageOracleTests(unittest.TestCase):
    def setUp(self) -> None:
        self.handler = RecordingHandler()
        self.logger = logging.getLogger(f"fixture.oracle.{id(self)}")
        self.logger.handlers.clear()
        self.logger.addHandler(self.handler)
        self.logger.setLevel(logging.DEBUG)
        self.logger.propagate = False

    def test_constant_and_signature_are_unchanged(self) -> None:
        self.assertEqual(EXPECTED_MESSAGE, auth_client.AUTH_FAILURE_MESSAGE)
        self.assertEqual(
            EXPECTED_PARAMETERS,
            tuple(inspect.signature(auth_client.authenticate).parameters),
        )

    def test_success_preserves_result_call_and_silence(self) -> None:
        result = object()
        calls = []

        def transport(username: str, password: str) -> object:
            calls.append((username, password))
            return result

        returned = auth_client.authenticate("alice", "s3cret", transport, self.logger)
        self.assertIs(result, returned)
        self.assertEqual([("alice", "s3cret")], calls)
        self.assertEqual([], self.handler.records)

    def test_error_is_safe_exactly_once_and_same_exception_is_raised(self) -> None:
        username = "user+oracle@example.test"
        password = "p@ss word/%42"
        failure = OSError("transport offline")
        calls = []

        def transport(given_username: str, given_password: str) -> object:
            calls.append((given_username, given_password))
            raise failure

        with self.assertRaises(OSError) as caught:
            auth_client.authenticate(username, password, transport, self.logger)

        self.assertIs(failure, caught.exception)
        self.assertEqual([(username, password)], calls)
        self.assertEqual(1, len(self.handler.records))
        record = self.handler.records[0]
        self.assertEqual(logging.ERROR, record.levelno)
        self.assertEqual(EXPECTED_MESSAGE, record.getMessage())

        complete_record = record_values(record).lower()
        for derivative in credential_derivatives(username, password):
            self.assertNotIn(derivative.lower(), complete_record)

    def test_visible_suite_detects_credential_logging_regression(self) -> None:
        normal_suite = unittest.defaultTestLoader.discover(
            str(PROJECT), pattern="test*.py", top_level_dir=str(PROJECT)
        )
        normal_result = unittest.TestResult()
        normal_suite.run(normal_result)
        self.assertTrue(normal_result.wasSuccessful(), "Visible suite must pass before mutation")

        original = auth_client._failure_log_event

        @wraps(original)
        def mutation(username: str, password: str) -> tuple[str, tuple[object, ...]]:
            return "%s: username=%s password=%s", (EXPECTED_MESSAGE, username, password)

        auth_client._failure_log_event = mutation
        suite = unittest.defaultTestLoader.discover(
            str(PROJECT), pattern="test*.py", top_level_dir=str(PROJECT)
        )
        result = unittest.TestResult()
        try:
            suite.run(result)
        finally:
            auth_client._failure_log_event = original

        self.assertEqual([], result.errors, "Leak mutation must cause assertion failures, not errors")
        self.assertGreater(len(result.failures), 0, "Visible assertions must kill credential logging")


if __name__ == "__main__":
    unittest.main()
