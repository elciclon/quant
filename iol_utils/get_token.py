import requests
import json


class Token:

    def __init__(self, user_data_file):

        # API Parameters
        self.__url = "https://api.invertironline.com/token"
        self.__grant_type = "password"
        self.__user_data_file = user_data_file
        self.__user_data = self.__load_user_data()

    def __load_user_data(self):
        try:
            with open(self.__user_data_file) as json_file:
                return json.load(json_file)
        except FileNotFoundError:
            raise Exception("User data file not found")
        except json.decoder.JSONDecodeError:
            raise Exception("Error decoding JSON file")

    def get_token(self) -> dict:
        """Get the token to be used in the requests

        Returns:
            str: Bearer token
        """
        try:
            data = {
                "username": self.__user_data[0]["username"],
                "password": self.__user_data[0]["password"],
                "grant_type": self.__grant_type,
            }

            response = requests.post(url=self.__url, data=data)

            # Check if the request was successful
            if response.status_code != 200:
                raise Exception(
                    f"Error fetching token: {response.status_code} {response.text}"
                )

            token = response.json().get("access_token")
            if not token:
                raise Exception("Error: 'access_token' not found in the response")

            return f"Bearer {token}"

        except requests.RequestException as e:
            raise Exception(f"HTTP Request failed: {e}")


# Example usage
# token_instance = Token("path_to_user_data.json")
# token = token_instance.get_token()
# print(token)
