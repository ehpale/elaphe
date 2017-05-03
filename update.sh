#!/usr/bin/env bash
set -euo pipefail
IFS=$'\n\t'

version='2017-04-04'
curl -fSL https://github.com/bwipp/postscriptbarcode/releases/download/$version/postscriptbarcode-monolithic-package-$version.tgz -o psbc.tgz

tar -zxC ./elaphe/postscriptbarcode/ -f psbc.tgz --strip=2 --no-anchored barcode.ps LICENSE README
rm psbc.tgz
