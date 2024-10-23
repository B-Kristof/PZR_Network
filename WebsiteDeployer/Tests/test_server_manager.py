import unittest
from unittest.mock import patch, Mock, MagicMock
import requests
from ServerManager.SSHServer import SSHServer

class TestConnect(unittest.TestCase):

    @patch("paramiko.SSHClient")
    @patch("paramiko.RSAKey.from_private_key_file")
    @patch("ErrorHandler.FatalErrorHandler.FatalError")
    def test_connect_success(self, mock_fatal_error, mock_rsa_key, mock_ssh_client):
        # Arrange
        ssh_client_instance = mock_ssh_client.return_value
        mock_rsa_key.return_value = MagicMock()  # Simulate the private key object
        connection_mock = MagicMock()

        # Act
        server = SSHServer("example.com", 22, "user", "private_key_path")
        with patch("ServerManager.Connection.Connection", return_value=connection_mock):
            connection = server.connect()

        # Assert
        mock_ssh_client.assert_called_once()
        ssh_client_instance.set_missing_host_key_policy.assert_called_once_with(mock_ssh_client.AutoAddPolicy())
        ssh_client_instance.connect.assert_called_once_with("example.com", 22, username="user",
                                                            pkey=mock_rsa_key.return_value)
        self.assertEqual(connection, connection_mock)


if __name__ == '__main__':
    unittest.main()