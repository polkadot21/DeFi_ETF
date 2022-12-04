import os
from typing import Final

from defi_etf import DeFiETF
from utils import (Assets, extract_day_of_week, extract_sma_features, extract_threshold_features)
from strategy import SmaCross, MLWalkForwardStrategy, Strategies
import backtesting

strategy_choice = assets_choice = os.getenv("strategy", "smacrossover")

if strategy_choice in Strategies.all:
    STRATEGY: Final = strategy_choice
else:
    raise NotImplementedError("This strategy is not implemented yet!")

FEES: Final = 0.01
CASH: Final = 10_000
MARGIN: Final = 0.05


def backtest():
    defi_etf = DeFiETF(assets=Assets)
    defi_etf.calculate_price(starting_date="365")

    df = defi_etf.price[["etf_price"]].copy()
    df["Open"] = df["Close"] = df["High"] = df["Low"] = df["etf_price"]
    df = df.drop(columns="etf_price")

    print("=========")
    print(STRATEGY)
    print("=========")

    if STRATEGY == "smacrossover":
        bt = backtesting.Backtest(df.iloc[:-1], SmaCross, cash=CASH, commission=FEES)
        stats = bt.run()
        print(stats)


    elif STRATEGY == "forecasting":
        extract_sma_features(df)
        extract_threshold_features(df, defi_etf.threshold)
        extract_day_of_week(df)
        df = df.dropna().astype(float)

        bt = backtesting.Backtest(df, MLWalkForwardStrategy, cash=CASH, commission=FEES, margin=MARGIN)

        stats = bt.run()
        print(stats)


if __name__ == "__main__":
    backtest()
