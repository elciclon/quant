import requests
from datetime import datetime
import json
import pandas as pd
from iol_utils.get_token import Token


class IOLRequest:
    def __init__(self, user_data_file: str) -> None:

        self.__url = "https://api.invertironline.com/api/v2"
        self.__accept = "application/json"
        self.__content_type = "application/x-www-form-urlencoded"
        self.__token = Token(user_data_file).get_token()
        self.headers_iol = {
            "Accept": self.__accept,
            "Content-Type": self.__content_type,
            "Authorization": self.__token,
        }

    def __parse_date(self, data) -> pd.DataFrame:
        df = pd.DataFrame(data)
        df["date"] = pd.to_datetime(df["fechaHora"]).dt.date
        df.set_index("date", inplace=True)
        df.drop(columns="fechaHora", inplace=True)
        return df

    def __format_date(self, date_str: str) -> str:
        return datetime.strptime(date_str, "%Y-%m-%d").date().isoformat()

    def __build_url(
        self, ticker: str, market: str, start_date: str, end_date: str, adjusted: bool
    ) -> str:
        adjusted = "ajustada" if adjusted else "sinAjustar"
        formatted_start_date = self.__format_date(start_date) if start_date else ""
        formatted_end_date = self.__format_date(end_date) if end_date else ""
        return f"{self.__url}/{market}/Titulos/{ticker}/Cotizacion/seriehistorica/{formatted_start_date}/{formatted_end_date}/{adjusted}"

    def get(
        self,
        ticker: str,
        market: str,
        start_date: str = None,
        end_date: str = None,
        adjusted: bool = False,
    ) -> json:

        url = self.__build_url(ticker, market, start_date, end_date, adjusted)
        response = requests.get(
            url=url,
            headers=self.headers_iol,
        )

        if response.status_code != 200:
            raise Exception(
                f"Error fetching data: {response.status_code} {response.text}"
            )

        if response.text == "[]":
            raise Exception("No data found")

        return self.__parse_date(response.json())


# Example usage
# iol_request = IOLRequest("path_to_user_data.json")
# data = iol_request.get(ticker="MIRG", market="bCBA", start_date="2021-01-01", end_date="2021-12-31")
# print(data)
