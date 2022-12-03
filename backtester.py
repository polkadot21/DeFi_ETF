from defi_etf import DeFiETF
from utils import Assets
from strategy import SmaCross
import backtesting


def backtest():
    defi_etf = DeFiETF(assets=Assets)
    defi_etf.calculate_price(starting_date="365")

    df = defi_etf.price[["etf_price"]].copy()
    df["Open"] = df["Close"] = df["High"] = df["Low"] = df["etf_price"]
    df = df.drop(columns="etf_price")

    bt = backtesting.Backtest(df.iloc[:-1], SmaCross, cash=10_000, commission=.01)
    stats = bt.run()
    print(stats)


if __name__ == "__main__":
    backtest()
