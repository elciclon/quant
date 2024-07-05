import unittest
from unittest.mock import patch, Mock, mock_open
import pandas as pd
from iol_utils.get_token import Token
from iol_utils.iol_requests import IOLRequest


class TestRequest(unittest.TestCase):

    @patch(
        "builtins.open",
        new_callable=mock_open,
        read_data='[{"username": "test_user", "password": "test_pass"}]',
    )
    @patch(
        "iol_utils.get_token.Token.get_token", return_value="Bearer mock_token"
    )  # Mock the get_token method
    def setUp(self, mock_get_token, mock_file):
        self.iol_request = IOLRequest("test_user_data.json")

    def test_initialization(self):
        self.assertEqual(
            self.iol_request.headers_iol["Authorization"], "Bearer mock_token"
        )

    def test_format_date(self):
        formatted_date = self.iol_request._IOLRequest__format_date("2021-01-01")
        self.assertEqual(formatted_date, "2021-01-01")

    def test_parse_date(self):
        data = [{"fechaHora": "2021-01-01T00:00:00", "value": 100}]
        parsed_df = self.iol_request._IOLRequest__parse_date(data)
        self.assertIsInstance(parsed_df, pd.DataFrame)
        self.assertIn("value", parsed_df.columns)
        self.assertEqual(parsed_df.index[0], pd.to_datetime("2021-01-01").date())

    @patch("requests.get")
    def test_get_success(self, mock_get):
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = [
            {"fechaHora": "2021-01-01T00:00:00", "value": 100}
        ]
        mock_get.return_value = mock_response

        data = self.iol_request.get(
            ticker="MIRG", market="bCBA", start_date="2021-01-01", end_date="2021-12-31"
        )
        self.assertIsInstance(data, pd.DataFrame)
        self.assertIn("value", data.columns)

    @patch("requests.get")
    def test_get_no_data(self, mock_get):
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.text = "[]"
        mock_get.return_value = mock_response

        with self.assertRaises(Exception) as context:
            self.iol_request.get(
                ticker="MIRG",
                market="bCBA",
                start_date="2021-01-01",
                end_date="2021-12-31",
            )

        self.assertTrue("No data found" in str(context.exception))

    @patch("requests.get")
    def test_get_api_error(self, mock_get):
        mock_response = Mock()
        mock_response.status_code = 500
        mock_response.text = "Internal Server Error"
        mock_get.return_value = mock_response

        with self.assertRaises(Exception) as context:
            self.iol_request.get(
                ticker="MIRG",
                market="bCBA",
                start_date="2021-01-01",
                end_date="2021-12-31",
            )

        self.assertTrue("Error fetching data" in str(context.exception))


if __name__ == "__main__":
    unittest.main()
