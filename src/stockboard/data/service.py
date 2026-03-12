from datetime import date

from yfinance import Ticker
from yfinance import exceptions as yf_exceptions

from stockboard.data.exceptions import NoDataError, RateLimitError
from stockboard.data.schemas import TickerResponse
from stockboard.data.types import OHLCV, Interval


def get_ticker_data(
    ticker: str,
    from_date: date,
    to_date: date,
    interval: Interval,
) -> TickerResponse:
    """Get historical data for a given ticker and date range."""
    t = Ticker(ticker.upper())

    try:
        df = t.history(start=from_date, end=to_date, interval=interval.yf)
    except yf_exceptions.YFRateLimitError as e:
        raise RateLimitError()
    except Exception as e:
        raise Exception("Error fetching historical data")

    if df.empty:
        raise NoDataError("No data found. Please check the ticker and date range.")

    data = [
        OHLCV(
            t=int(ts.timestamp()),
            o=round(row["Open"], 4),
            h=round(row["High"], 4),
            l=round(row["Low"], 4),
            c=round(row["Close"], 4),
            v=int(row["Volume"]),
        )
        for ts, row in df.iterrows()
    ]

    return TickerResponse(ticker=ticker.upper(), interval=interval, from_date=from_date, to_date=to_date, data=data)
