"""
Download historical cryptocurrency market data from the Binance REST API.

Run from the command line with:
    python fetch_binance_data.py
    python fetch_binance_data.py --symbol ETHUSDT --interval 15m
"""

import argparse
import requests
import pandas as pd
import os


BINANCE_KLINES_URL = "https://api.binance.com/api/v3/klines"
MIN_LIMIT = 1
MAX_LIMIT = 1000


def fetch_klines(symbol="BTCUSDT", interval="1h", limit=500):
    """Fetch OHLCV kline data from the Binance REST API."""
    params = {
        "symbol": symbol,
        "interval": interval,
        "limit": limit,
    }

    response = requests.get(BINANCE_KLINES_URL, params=params, timeout=30)
    response.raise_for_status()
    return response.json()


def convert_to_dataframe(klines):
    """Convert the raw Binance kline response into a pandas DataFrame."""
    columns = [
        "open_time",
        "open",
        "high",
        "low",
        "close",
        "volume",
        "close_time",
        "quote_asset_volume",
        "number_of_trades",
        "taker_buy_base_asset_volume",
        "taker_buy_quote_asset_volume",
        "ignore",
    ]

    df = pd.DataFrame(klines, columns=columns)

    # Convert millisecond timestamps into readable datetimes.
    df["open_time"] = pd.to_datetime(df["open_time"], unit="ms")
    df["close_time"] = pd.to_datetime(df["close_time"], unit="ms")

    # Convert numeric market fields from strings to numeric types.
    numeric_columns = [
        "open",
        "high",
        "low",
        "close",
        "volume",
        "quote_asset_volume",
        "number_of_trades",
        "taker_buy_base_asset_volume",
        "taker_buy_quote_asset_volume",
    ]
    df[numeric_columns] = df[numeric_columns].apply(pd.to_numeric)

    return df


def save_to_csv(dataframe, filename="btcusdt_1h.csv"):
    """Save the DataFrame to a CSV file."""
    dataframe.to_csv(filename, index=False)


def parse_arguments():
    """Parse command line arguments for symbol, interval, and candle limit."""
    parser = argparse.ArgumentParser(
        description="Download historical OHLCV cryptocurrency data from Binance."
    )
    parser.add_argument(
        "--symbol",
        default="BTCUSDT",
        help="Trading pair symbol to download, for example BTCUSDT or ETHUSDT.",
    )
    parser.add_argument(
        "--interval",
        default="1h",
        help="Kline interval, for example 1h, 15m, or 1d.",
    )
    parser.add_argument(
        "--limit",
        type=int,
        default=500,
        help="Number of candles to download. Binance allows 1 to 1000. Default is 500.",
    )
    args = parser.parse_args()

    if not MIN_LIMIT <= args.limit <= MAX_LIMIT:
        parser.error(
            f"--limit must be between {MIN_LIMIT} and {MAX_LIMIT}. "
            f"Received: {args.limit}"
        )

    return args


def main():
    """Fetch, transform, save, and preview Binance market data."""
    args = parse_arguments()

    try:
        # Fetch raw candle data using the user-provided or default CLI arguments.
        klines = fetch_klines(
            symbol=args.symbol,
            interval=args.interval,
            limit=args.limit,
        )
        dataframe = convert_to_dataframe(klines)

        # Ensure the data directory exists
        os.makedirs("data", exist_ok=True)

        output_filename = os.path.join(
            "data",
            f"{args.symbol.lower()}_{args.interval}.csv"
        )
        save_to_csv(dataframe, filename=output_filename)

        # Display the first five rows so the user can verify the output quickly.
        print(dataframe.head())
    except requests.exceptions.RequestException as error:
        print(f"Failed to fetch data from Binance API: {error}")
    except ValueError as error:
        print(f"Failed to process Binance data: {error}")


if __name__ == "__main__":
    main()
