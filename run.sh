#!/bin/bash
# exit when any command fails
set -e

# shellcheck disable=SC2162

export assets=$1
export strategy=$2

echo "You've chosen the following assets: $assets"
echo "and the following strategy: $strategy"

python3 downloader.py && python3 backtester.py
