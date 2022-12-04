#!/bin/bash
# exit when any command fails
set -e

# shellcheck disable=SC2162
echo "$1"
export assets=$1
echo "You've chosen the following assets: $assets"

python3 downloader.py && python3 backtester.py
