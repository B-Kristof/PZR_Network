import unittest
from unittest.mock import patch, mock_open, MagicMock
from cryptography.fernet import Fernet
from io import BytesIO
from KeyManager.Encrypter import encrypt_file, decrypt_file


class TestFileEncryption(unittest.TestCase):

    # SUCCESS
    @patch("builtins.open", new_callable=mock_open)
    @patch("cryptography.fernet.Fernet.encrypt")
    @patch("ErrorHandler.FatalErrorHandler.FatalError")
    def test_encrypt_file_success(self, mock_fatal_error, mock_encrypt, mock_file_open):
        # Arrange
        encryption_key = Fernet.generate_key()
        input_data = b"test data"
        encrypted_data = b"encrypted data"

        mock_file_open.side_effect = [BytesIO(input_data), BytesIO()]
        mock_encrypt.return_value = encrypted_data

        # Act
        encrypt_file("input.txt", "output.txt", encryption_key)

        # Assert
        mock_file_open.assert_any_call("input.txt", "rb")
        mock_file_open.assert_any_call("output.txt", "wb")
        mock_encrypt.assert_called_once_with(input_data)
        self.assertFalse(mock_fatal_error.called)

    # EDGE CASES
    # File not found
    @patch("builtins.open", side_effect=FileNotFoundError)
    @patch("ErrorHandler.FatalErrorHandler.FatalError")
    def test_encrypt_file_file_not_found(self, mock_fatal_error, mock_file_open):
        # Arrange
        encryption_key = Fernet.generate_key()

        # Act
        encrypt_file("nonexistent.txt", "output.txt", encryption_key)

        # Assert
        mock_file_open.assert_called_once_with("nonexistent.txt", "rb")
        mock_fatal_error.assert_called_once()

    # General exception
    @patch("builtins.open", new_callable=mock_open)
    @patch("cryptography.fernet.Fernet.encrypt", side_effect=Exception("Encryption Error"))
    @patch("ErrorHandler.FatalErrorHandler.FatalError")
    def test_encrypt_file_general_exception(self, mock_fatal_error, mock_encrypt, mock_file_open):
        # Arrange
        encryption_key = Fernet.generate_key()
        input_data = b"test data"
        mock_file_open.side_effect = [BytesIO(input_data), BytesIO()]

        # Act
        encrypt_file("input.txt", "output.txt", encryption_key)

        # Assert
        mock_encrypt.assert_called_once()
        mock_fatal_error.assert_called_once()


class TestFileDecryption(unittest.TestCase):

    # SUCCESS
    @patch("builtins.open", new_callable=mock_open)
    @patch("cryptography.fernet.Fernet.decrypt")
    @patch("ErrorHandler.FatalErrorHandler.FatalError")
    def test_decrypt_file_success(self, mock_fatal_error, mock_decrypt, mock_file_open):
        # Arrange
        encryption_key = Fernet.generate_key()
        encrypted_data = b"encrypted data"
        decrypted_data = b"test data"

        mock_file_open.side_effect = [BytesIO(encrypted_data), BytesIO()]
        mock_decrypt.return_value = decrypted_data

        # Act
        decrypt_file("input.txt", "output.txt", encryption_key)

        # Assert
        mock_file_open.assert_any_call("input.txt", "rb")
        mock_file_open.assert_any_call("output.txt", "wb")
        mock_decrypt.assert_called_once_with(encrypted_data)
        self.assertFalse(mock_fatal_error.called)

    # EDGE CASES
    # File not found
    @patch("builtins.open", side_effect=FileNotFoundError)
    @patch("ErrorHandler.FatalErrorHandler.FatalError")
    def test_decrypt_file_file_not_found(self, mock_fatal_error, mock_file_open):
        # Arrange
        encryption_key = Fernet.generate_key()

        # Act
        decrypt_file("nonexistent.txt", "output.txt", encryption_key)

        # Assert
        mock_file_open.assert_called_once_with("nonexistent.txt", "rb")
        mock_fatal_error.assert_called_once()

    # General exception
    @patch("builtins.open", new_callable=mock_open)
    @patch("cryptography.fernet.Fernet.decrypt", side_effect=Exception("Decryption Error"))
    @patch("ErrorHandler.FatalErrorHandler.FatalError")
    def test_decrypt_file_general_exception(self, mock_fatal_error, mock_decrypt, mock_file_open):
        # Arrange
        encryption_key = Fernet.generate_key()
        encrypted_data = b"encrypted data"
        mock_file_open.side_effect = [BytesIO(encrypted_data), BytesIO()]

        # Act
        decrypt_file("input.txt", "output.txt", encryption_key)

        # Assert
        mock_decrypt.assert_called_once()
        mock_fatal_error.assert_called_once()


if __name__ == "__main__":
    unittest.main()
