import os
from typing import List, Final
import json
from utils import Collectable
from abc import ABC, abstractmethod


class DeFi(Collectable):
    def __init__(self):
        super().__init__()
        self._category = "decentralized-finance-defi"


class EthereumEcoSystem(Collectable):
    def __init__(self):
        super().__init__()
        self._category = "ethereum-ecosystem"

    @property
    def key_words(self):
        return ("staked", "liquid")


class Stable(Collectable):
    def __init__(self):
        super().__init__()
        self._category = "stablecoins"

    @property
    def key_words(self):
        return ("usd", "dai")


class Wrapped(Collectable):
    def __init__(self):
        super().__init__()
        self._category = "wrapped-tokens"


class AssetCollector(ABC):

    @property
    @abstractmethod
    def assets(self):
        raise NotImplementedError

    @abstractmethod
    def collect(self):
        raise NotImplementedError


class EthDeFiAssetCollector(AssetCollector):
    SAVE_PATH: Final = "data/assets.json"
    N_ASSETS: Final = 12

    def __init__(self, included_assets: List[List[str]], excluded_assets: List[List[str]],
                 negative_keywords: List[str]):
        self._included_assets: List[List[str]] = included_assets
        self._excluded_assets: List[List[str]] = excluded_assets
        self._negative_keywords: List[str] = negative_keywords

        self._flatten_included_assets()
        self._flatten_excluded_assets()
        self._existed_assets = None
        self._collected_assets = None

    @property
    def assets(self):
        return self._collected_assets

    def collect(self):
        self._collected_assets = [asset for asset in self._included_assets if asset not in self._excluded_assets \
                                  and not (any(keyword in asset for keyword in self._negative_keywords))]

    def save(self):
        if self._is_file():
            self._open()
            self._add_downloaded_assets_to_existent()
        else:
            self._existed_assets = self._default_dict
        with open(self.SAVE_PATH, 'w') as fp:
            json.dump(self._existed_assets, fp)

    def _flatten_included_assets(self):
        # TODO: implement for more than two lists
        self._check_included_assets()
        set_of_assets = frozenset(self._included_assets[1])
        self._included_assets = [asset for asset in self._included_assets[0] if asset in set_of_assets]

    def _flatten_excluded_assets(self):
        self._excluded_assets = [asset for excluded_assets in self._excluded_assets for asset in excluded_assets]

    def _check_included_assets(self):
        if len(self._included_assets) != 2:
            raise NotImplementedError("The list must contain two categories of assets.")

    def _is_file(self):
        return os.path.isfile(self.SAVE_PATH)

    def _open(self):
        with open(self.SAVE_PATH) as f:
            self._existed_assets = json.load(f)

    def _add_downloaded_assets_to_existent(self):
        self._existed_assets.update(self._default_dict)

    @property
    def _default_dict(self):
        return {"default": self._collected_assets[:self.N_ASSETS]}


def collect_and_save():
    defi = DeFi()
    defi.collect()

    eth = EthereumEcoSystem()
    eth.collect()

    wrapper_tokens = Wrapped()
    wrapper_tokens.collect()

    stable_coins = Stable()
    stable_coins.collect()

    negative_keywords = []
    for neg_word in eth.key_words:
        negative_keywords.append(neg_word)

    for neg_word in stable_coins.key_words:
        negative_keywords.append(neg_word)

    collector = EthDeFiAssetCollector(included_assets=[eth.assets, defi.assets],
                                      excluded_assets=[stable_coins.assets, wrapper_tokens.assets],
                                      negative_keywords=negative_keywords)

    collector.collect()
    collector.save()


if __name__ == "__main__":
    collect_and_save()
