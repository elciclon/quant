import requests
import json


class Token:

    def __init__(self, user_data):

        # API Parameters
        self.__url = "https://api.invertironline.com/token"
        self.__content_type = "application/x-www-form-urlencoded"
        self.__granttype = "password"
        self.__accept = "application/json"
        self.__user_data_file = user_data

        try:
            with open(self.__user_data_file) as json_file:
                self.__user_data = json.load(json_file)
        except FileNotFoundError:
            raise Exception("User data file not found")
        except json.decoder.JSONDecodeError:
            raise Exception("Error decoding JSON file")

    def get_token(self) -> dict:
        """Get the token to be used in the requests

        Returns:
            dict: token
        """
        try:
            data = {
                "username": self.__user_data[0]["username"],
                "password": self.__user_data[0]["password"],
                "grant_type": self.__granttype,
            }

            r = requests.post(url=self.__url, data=data)

            # Check if the request was successful
            if r.status_code != 200:
                raise Exception(f"Error fetching token: {r.status_code} {r.text}")

            self.__bearer_token = "Bearer " + str(r.json()["access_token"])
            return {
                "Accept": self.__accept,
                "Content-Type": self.__content_type,
                "Authorization": self.__bearer_token,
            }
        except KeyError:
            raise Exception("Error: 'access_token' not found in the response")
        except requests.RequestException as e:
            raise Exception(f"HTTP Request failed: {e}")
