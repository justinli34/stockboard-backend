from zoneinfo import ZoneInfo

from yfinance import Ticker
from yfinance import exceptions as yf_exceptions

from stockboard.stocks.exceptions import NoDataError, RateLimitError
from stockboard.stocks.models import OHLCV, PricePoint, Quote, Range


def _fetch_history(ticker: Ticker, period: str, interval: str):
    try:
        df = ticker.history(period=period, interval=interval)
    except yf_exceptions.YFRateLimitError:
        raise RateLimitError()
    except Exception:
        raise Exception("Error fetching historical data")

    if df.empty:
        raise NoDataError("No data found. Please check the ticker and date range.")

    return df


def fetch_ohlcv(ticker: str, range: Range) -> list[OHLCV]:
    df = _fetch_history(Ticker(ticker.upper()), period=range.period, interval=range.interval)

    return [
        OHLCV(
            time=ts.astimezone(ZoneInfo("America/New_York")).isoformat(),
            o=round(row["Open"], 2),
            h=round(row["High"], 2),
            l=round(row["Low"], 2),
            c=round(row["Close"], 2),
            v=int(row["Volume"]),
        )
        for ts, row in df.iterrows()
    ]


def fetch_quote(ticker: str) -> Quote:
    df = _fetch_history(Ticker(ticker.upper()), period="2d", interval="1d")

    current_price = df["Close"].iloc[-1]
    prev_close = df["Close"].iloc[0]
    daily_return = current_price - prev_close
    daily_return_pct = (daily_return / prev_close) * 100

    return Quote(
        current_price=round(current_price, 2),
        daily_return=round(daily_return, 2),
        daily_return_pct=round(daily_return_pct, 2),
    )


def fetch_preview_data(ticker: str) -> list[PricePoint]:
    df = _fetch_history(Ticker(ticker.upper()), period="1d", interval="5m")

    return [
        PricePoint(
            time=ts.astimezone(ZoneInfo("America/New_York")).isoformat(),
            price=round(row["Close"], 2),
        )
        for ts, row in df.iterrows()
    ]
