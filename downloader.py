import json
from typing import Final

from pycoingecko import CoinGeckoAPI

from utils import Assets


class DownloaderAndSaver(CoinGeckoAPI):
    def __init__(self):
        super().__init__()
        self._currency: Final = "usd"
        self._n_days: Final = 365

    def download_and_save(self, asset_id: str):
        prices_and_mcap = self.get_coin_market_chart_by_id(id=[asset_id],
                                                           vs_currency='usd',
                                                           days=self._n_days)

        with open("data/" + asset_id + ".json", 'w') as fp:
            json.dump(prices_and_mcap, fp)
            print(f"Saved: {asset_id} for {self._n_days}")


if __name__ == "__main__":
    downloader = DownloaderAndSaver()
    for asset in Assets.names:
        downloader.download_and_save(asset_id=asset)
