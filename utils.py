from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Union
import pandas as pd
from pyhere import here
from typing import Final
import json
import os
from pycoingecko import CoinGeckoAPI

assets_choice = os.getenv("assets", "default")

print("============")
print("Set assets to:")
print(assets_choice)
print("============")

ASSETS_PATH: Final = here("data", "assets.json")

if assets_choice == "default":
    with open(ASSETS_PATH) as assets_json:
        ASSETS: Final = json.load(assets_json)["default"]
elif assets_choice.lower() == "defipulse":
    with open(ASSETS_PATH) as assets_json:
        ASSETS: Final = json.load(assets_json)["DeFiPulse"]
else:
    raise NotImplementedError("Other assets will be implemented in the future!")


@dataclass
class Assets:
    names = ASSETS


@dataclass
class Weights:
    asset_to_weight: dict


class ETF(ABC):
    def __init__(self, assets: Assets):
        self._assets: Assets = assets
        self._historical_price: Union[pd.DataFrame, None] = None

    @property
    @abstractmethod
    def price(self):
        return self._historical_price

    @abstractmethod
    def calculate_price(self, starting_date: str):
        raise NotImplementedError


@dataclass
class TempDF:
    df: pd.DataFrame

    def set_date(self):
        self.df["date"] = self.df[self.df.columns[0]].apply(lambda x: x[0])
        self.df["date"] = pd.to_datetime(self.df['date'], unit='ms')
        # self.df["date"] = self.df["date"].apply(lambda x: x.date())

    def extract_value(self):
        for column in self.df.columns:
            if column != "date":
                self.df[column] = self.df[column].apply(lambda x: x[1])


@dataclass
class Historical:
    market_caps: dict
    prices: dict

    def to_df(self):
        df = pd.DataFrame()
        for _dict in self.__dict__.values():
            if isinstance(_dict, dict):
                temp = TempDF(df=pd.DataFrame.from_dict(_dict))
                temp.set_date()
                temp.df = temp.df.set_index("date", drop=True)
                temp.extract_value()
                df = pd.concat([df, temp.df], axis=1)
        return df


# TODO: implement error handling for ids
class Collectable(ABC, CoinGeckoAPI):
    def __init__(self):
        super().__init__()
        self._assets = []
        self._category = None
        self._currency = "usd"
        self._order = "market_cap_desc"

    @property
    def assets(self):
        return self._assets

    def collect(self):
        coins = self.get_coins_markets(vs_currency=self._currency, category=self._category, order=self._order)
        for coin in coins:
            self._assets.append(coin["id"])
