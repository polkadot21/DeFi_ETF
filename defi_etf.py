from utils import ETF, Assets, Historical, Threshold
import json
from utils import SMA

class DeFiETF(ETF):
    N_STD = 2
    N_LOOKBACK = 20

    def __init__(self, assets: Assets):
        super().__init__(assets)
        self._raw_historical_price: Historical = Historical({}, {})
        self._load_data()
        self._historical_price = self._raw_historical_price.to_df()

        self._threshold: Threshold = Threshold(0, 0)

    @property
    def price(self):
        return self._historical_price

    @property
    def threshold(self):
        return self._threshold

    def calculate_price(self, starting_date: str):
        self._calculate_total_market_cap()
        self._calculate_weight()
        self._calculate_weighted_price()
        self._calculate_etf_price()
        self._calculate_threshold()

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

    def _calculate_threshold(self):
        mean = self._historical_price["etf_price"].rolling(self.N_LOOKBACK).mean()
        std = self._historical_price["etf_price"].rolling(self.N_LOOKBACK).std()
        self._threshold.upper = mean + self.N_STD * std
        self._threshold.lower = mean - self.N_STD * std
