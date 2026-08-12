# tests/test_password.py
#
# Kept as a class-based (unittest.TestCase) reference, deliberately —
# see tests/test_user.py or test_auth.py for the plain-function/pytest-fixture
# style used elsewhere in this project. Both styles work with pytest;
# this file exists to compare them side by side later.

import unittest
from app.utils.password import hash_password, verify_password


class PasswordHashingTests(unittest.TestCase):
    def setUp(self) -> None:
        # unittest.TestCase equivalent of a pytest fixture — but this runs
        # fresh before EVERY test method below, not once for the whole class.
        # Nothing is shared/cached across tests; each gets a clean self.password
        # and self.hash_password.
        self.password = "secret123"
        self.hash_password = hash_password(self.password)

    def test_hash_password_returns_different_string(self) -> None:
        # a hash should never equal the original plaintext — if it did,
        # you'd effectively be storing passwords in plain text
        assert self.hash_password != self.password

    def test_verify_password_accepts_correct_password(self) -> None:
        # round-trip check: the SAME password used to create the hash
        # must verify successfully against it
        assert verify_password(self.password, self.hash_password) is True

    def test_verify_password_rejects_wrong_password(self) -> None:
        # NOTE: earlier version of this test had a bug — it used the string
        # literal "self.password" (9 literal characters) instead of the
        # actual self.password attribute. It still passed, but for the
        # wrong reason — it wasn't really testing "wrong password rejected,"
        # just "this unrelated literal string doesn't match." Fixed below.
        assert verify_password("wrong-password", self.hash_password) is False

    def test_hash_password_produces_different_hash_each_time(self) -> None:
        # security property: good hashing (argon2/bcrypt) salts automatically,
        # so hashing the SAME password twice must produce DIFFERENT output.
        # If this ever failed, it would mean salting broke — a real,
        # catchable security regression.
        hash1 = hash_password(self.password)
        hash2 = hash_password(self.password)
        assert hash1 != hash2