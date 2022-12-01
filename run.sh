#!/bin/bash
# exit when any command fails
set -e

echo -e "Enter the list of assets or 'default'
*Remember that the assets must be consistent with Coingecko ids"
# shellcheck disable=SC2162
read assets
export assets
echo "You've chosen the following assets: $assets"

python3 downloader.py && python3 backtester.py
