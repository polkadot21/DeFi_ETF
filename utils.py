from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Union
import pandas as pd
from pyhere import here
from typing import Final
import json
import os
from pycoingecko import CoinGeckoAPI
import numpy as np

assets_choice = os.getenv("assets", "defipulse")

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


@dataclass
class Threshold:
    upper: float
    lower: float


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


def SMA(values, n):
    """
    Return simple moving average of `values`, at
    each step taking into account `n` previous values.
    """
    return pd.Series(values).rolling(n).mean()


def get_X(data):
    """Return model design matrix X"""
    return data.filter(like='X').values


def get_y(data):
    """Return dependent variable y"""
    y = data.Close.pct_change(48).shift(-48)  # Returns after roughly two days
    y[y.between(-.004, .004)] = 0  # Devalue returns smaller than 0.4%
    y[y > 0] = 1
    y[y < 0] = -1
    return y


def get_clean_Xy(df):
    """Return (X, y) cleaned of NaN values"""
    X = get_X(df)
    y = get_y(df).values
    isnan = np.isnan(y)
    X = X[~isnan]
    y = y[~isnan]
    return X, y


def extract_sma_features(df: pd.DataFrame):
    SMA_LENGTH: Final = (10, 20, 50, 100)
    smas = []
    close = df.Close.values
    for length in SMA_LENGTH:
        smas.append(SMA(df.Close, length))
        df[f"X_SMA{SMA_LENGTH}"] = close - SMA(df.Close, length) / close


def extract_threshold_features(df: pd.DataFrame, threshold: Threshold):
    # Indicator features
    close = df.Close.values
    df['X_MOM'] = df.Close.pct_change(periods=2)
    df['X_BB_upper'] = (threshold.upper - close) / close
    df['X_BB_lower'] = (threshold.lower - close) / close
    df['X_BB_width'] = (threshold.upper - threshold.lower) / close


def extract_day_of_week(df: pd.DataFrame):
    df['X_day'] = df.index.dayofweek
