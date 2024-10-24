import unittest
from unittest.mock import patch, Mock
import requests
from WebsiteMonitor.Pinger import ping_target


class TestPingTarget(unittest.TestCase):

    @patch('requests.get')  # Mock the requests.get method
    def test_ping_success(self, mock_get):
        # Mocking a successful response (status code 200)
        mock_response = Mock()
        mock_response.status_code = 200
        mock_get.return_value = mock_response

        result = ping_target("http://example.com")
        self.assertTrue(result)

    @patch('requests.get')
    def test_ping_non_200_status(self, mock_get):
        # Mocking a non-successful response (e.g., status code 404)
        mock_response = Mock()
        mock_response.status_code = 404
        mock_get.return_value = mock_response

        result = ping_target("http://example.com")
        self.assertFalse(result)

    @patch('requests.get')
    def test_ping_timeout(self, mock_get):
        # Mocking a timeout exception
        mock_get.side_effect = requests.exceptions.ConnectTimeout

        result = ping_target("http://example.com")
        self.assertFalse(result)


if __name__ == '__main__':
    unittest.main()