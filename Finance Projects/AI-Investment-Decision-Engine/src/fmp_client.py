import requests


class FMPClient:

    BASE_URL = "https://financialmodelingprep.com/stable"

    def __init__(self, api_key):
        self.api_key = api_key


    def _get(self, endpoint, params=None):

        if params is None:
            params = {}

        params["apikey"] = self.api_key

        url = f"{self.BASE_URL}/{endpoint}"

        response = requests.get(
            url,
            params=params
        )

        response.raise_for_status()

        return response.json()


    def get_profile(self, symbol):

        return self._get(
            "profile",
            {
                "symbol": symbol
            }
        )


    def get_income_statement(self, symbol):

        return self._get(
            "income-statement",
            {
                "symbol": symbol,
                "period": "annual"
            }
        )


    def get_balance_sheet(self, symbol):

        return self._get(
            "balance-sheet-statement",
            {
                "symbol": symbol,
                "period": "annual"
            }
        )


    def get_cash_flow(self, symbol):

        return self._get(
            "cash-flow-statement",
            {
                "symbol": symbol,
                "period": "annual"
            }
        )


    def get_ratios(self, symbol):

        return self._get(
            "ratios",
            {
                "symbol": symbol,
                "period": "annual"
            }
        )