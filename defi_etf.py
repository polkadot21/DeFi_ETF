from utils import ETF, Assets, Historical
import json


class DeFiETF(ETF):
    def __init__(self, assets: Assets):
        super().__init__(assets)
        self._raw_historical_price: Historical = Historical({}, {})
        self._load_data()
        self._historical_price = self._raw_historical_price.to_df()

    @property
    def price(self):
        return self._historical_price

    def calculate_price(self, starting_date: str):
        self._calculate_total_market_cap()
        self._calculate_weight()
        self._calculate_weighted_price()
        self._calculate_etf_price()

    def _load_data(self):
        for asset in self._assets.names:
            with open("data/" + asset + ".json") as file_json:
                file = json.load(file_json)
                self._raw_historical_price.market_caps.update({asset + "_market_cap": file["market_caps"]})
                self._raw_historical_price.prices.update({asset + "_price": file["prices"]})

    def _calculate_total_market_cap(self):
        market_cap_columns = [column for column in self._historical_price.columns if "market_cap" in column]
        self._historical_price["total_market_cap"] = self._historical_price[market_cap_columns].sum(axis=1)

    def _calculate_weight(self):
        for column in self._historical_price.columns:
            if "market_cap" in column:
                self._historical_price[column + "_weight"] = self._historical_price[column] / self._historical_price[
                    "total_market_cap"]

    def _calculate_weighted_price(self):
        for asset in Assets.names:
            self._historical_price[asset + "_weighted_price"] = self._historical_price[asset + "_market_cap_weight"] * \
                                                                self._historical_price[asset + "_price"]

    def _calculate_etf_price(self):
        weighted_price_columns = [column for column in self._historical_price.columns if "weighted_price" in column]
        self._historical_price["etf_price"] = self._historical_price[weighted_price_columns].sum(axis=1)

