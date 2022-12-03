#!/bin/bash
# exit when any command fails
set -e

echo -e "Enter either 'default' or 'DeFiPulse'
*In the future more options will be supported"
# shellcheck disable=SC2162
read assets
export assets
echo "You've chosen the following assets: $assets"

python3 downloader.py && python3 backtester.py
