#!/usr/bin/env python3

import unittest
from authenticate import Authenticator

class TestAuthenticate(unittest.TestCase):
    def test_authenticate(self):
        auth = Authenticator()
        auth.insert_record("joseph", "1234")
        self.assertTrue(auth.authenticate_record("joseph", "1234"))
        self.assertFalse(auth.authenticate_record("joseph", "12345"))

def main():
    unittest.main()

if __name__ == "__main__":
    main()
