import unittest
from unittest.mock import patch, Mock
import json
import os
from iol_utils.get_token import Token


class TestToken(unittest.TestCase):

    def setUp(self):
        self.user_data_file = "test_user_data.json"

    def tearDown(self):
        # Remove the user data file after each test
        if os.path.exists(self.user_data_file):
            os.remove(self.user_data_file)

    @patch("iol_utils.get_token.requests.post")  # Mock the requests.post method
    def test_get_token_success(self, mock_post):
        # Prepare mock response
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"access_token": "mock_access_token"}
        mock_post.return_value = mock_response

        # Prepare user data
        user_data = [{"username": "test_user", "password": "test_password"}]

        with open(self.user_data_file, "w") as f:
            json.dump(user_data, f)

        # Create Token instance
        token_instance = Token(self.user_data_file)

        # Call get_token method
        token = token_instance.get_token()

        # Check the result
        self.assertEqual(
            token,
            "Bearer mock_access_token",
        )

    @patch("iol_utils.get_token.requests.post")  # Mock the requests.post method
    def test_get_token_failure(self, mock_post):
        # Prepare mock response
        mock_response = Mock()
        mock_response.status_code = 401
        mock_response.text = "Unauthorized"
        mock_post.return_value = mock_response

        # Prepare user data
        user_data = [{"username": "test_user", "password": "test_password"}]

        with open(self.user_data_file, "w") as f:
            json.dump(user_data, f)

        # Create Token instance
        token_instance = Token(self.user_data_file)

        # Call get_token method and check for exception
        with self.assertRaises(Exception) as context:
            token_instance.get_token()

        self.assertTrue("Error fetching token" in str(context.exception))


if __name__ == "__main__":
    unittest.main()
