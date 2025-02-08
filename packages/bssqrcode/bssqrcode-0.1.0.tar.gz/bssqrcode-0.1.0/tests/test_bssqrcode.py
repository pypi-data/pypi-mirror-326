import sys
import os
import unittest

# Ensure the test script finds bssqrcode properly
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from bssqrcode import bssqrcode
from cryptography.fernet import Fernet

class TestBssQRCode(unittest.TestCase):
    def setUp(self):
        self.key = bssqrcode.generate_key()
        self.data = "https://brewlock-auth.com/login"

    def test_encryption_decryption(self):
        encrypted = bssqrcode.encrypt_data(self.data, self.key)
        decrypted = bssqrcode.decrypt_data(encrypted, self.key)
        self.assertEqual(self.data, decrypted)

    def test_qr_creation_and_scan(self):
        file_path = "test_qr.png"
        bssqrcode.create_qr(self.data, self.key, file_path)
        self.assertTrue(os.path.exists(file_path))

if __name__ == "__main__":
    unittest.main()
