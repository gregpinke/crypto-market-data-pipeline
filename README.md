# Crypto Market Data Pipeline

![Python](https://img.shields.io/badge/python-3.x-blue)
![API](https://img.shields.io/badge/API-Binance-orange)
![License](https://img.shields.io/badge/license-MIT-green)

A simple Python project for downloading historical cryptocurrency OHLCV market data from the Binance REST API.

## Features

- Fetch market candle data
- Convert data into pandas DataFrame
- Export clean CSV datasets
- Command line arguments for symbol, interval, and candle count

## Installation

Install dependencies:

pip install -r requirements.txt

## Usage

Default usage:

python src/fetch_binance_data.py

Custom example:

python src/fetch_binance_data.py --symbol ETHUSDT --interval 15m --limit 500

## Output

The script saves a CSV file in the `data/` folder.

Example:

data/btcusdt_1h.csv

## Project Structure

crypto-market-data-pipeline/
│
├── src/
│   └── fetch_binance_data.py
├── data/
├── examples/
├── README.md
└── requirements.txt