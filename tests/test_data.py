import json
import sys
from typing import Final
from pyhere import here

sys.path.append(str(here().resolve()))
UNISWAP: Final = here("data", "uniswap.json")
YEARN_FINANCE: Final = here("data", "yearn-finance.json")


class TestData:
    KNOWN_KEYS: Final = ["prices", "market_caps", "total_volumes"]

    def test_data_keys(self):
        with open(UNISWAP) as file_json:
            file = json.load(file_json)
            assert list(file.keys()) == self.KNOWN_KEYS

    def test_equal_length(self):
        with open(UNISWAP) as file_json:
            uniswap = json.load(file_json)

        with open(YEARN_FINANCE) as file_json:
            yearn_finance = json.load(file_json)

        assert len(uniswap["market_caps"]) == len(yearn_finance["market_caps"])
