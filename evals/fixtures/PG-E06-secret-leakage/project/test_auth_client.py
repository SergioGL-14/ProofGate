"""Visible tests for the authentication boundary."""

import logging
import unittest

import auth_client


class AuthenticationTests(unittest.TestCase):
    def setUp(self) -> None:
        self.logger = logging.getLogger(f"fixture.visible.{id(self)}")
        self.logger.handlers.clear()
        self.logger.addHandler(logging.NullHandler())
        self.logger.propagate = False

    def test_returns_transport_result(self) -> None:
        token = object()
        self.assertIs(token, auth_client.authenticate("user", "pass", lambda _u, _p: token, self.logger))

    def test_supplies_credentials_to_transport_once(self) -> None:
        calls = []

        def transport(username: str, password: str) -> str:
            calls.append((username, password))
            return "token"

        auth_client.authenticate("Ada", "correct horse", transport, self.logger)
        self.assertEqual([("Ada", "correct horse")], calls)

    def test_transport_error_is_propagated(self) -> None:
        failure = OSError("offline")

        def transport(_username: str, _password: str) -> object:
            raise failure

        with self.assertRaises(OSError) as caught:
            auth_client.authenticate("user", "secret", transport, self.logger)
        self.assertIs(failure, caught.exception)


if __name__ == "__main__":
    unittest.main()
