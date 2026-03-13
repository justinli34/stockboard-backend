from datetime import datetime
from zoneinfo import ZoneInfo

from yfinance import Ticker
from yfinance import exceptions as yf_exceptions

from stockboard.stocks.exceptions import NoDataError, RateLimitError
from stockboard.stocks.models import OHLCV, Interval, TickerDailySnapshot


def get_ohlcv(
    ticker: str,
    from_time: datetime,
    to_time: datetime,
    interval: Interval,
) -> list[OHLCV]:
    """Get historical data for a given ticker and date range."""
    t = Ticker(ticker.upper())

    try:
        df = t.history(start=from_time, end=to_time, interval=interval.yf)
    except yf_exceptions.YFRateLimitError:
        raise RateLimitError()
    except Exception:
        raise Exception("Error fetching historical data")

    if df.empty:
        raise NoDataError("No data found. Please check the ticker and date range.")

    return [
        OHLCV(
            t=ts.astimezone(ZoneInfo("America/New_York")).isoformat(),
            o=round(row["Open"], 2),
            h=round(row["High"], 2),
            l=round(row["Low"], 2),
            c=round(row["Close"], 2),
            v=int(row["Volume"]),
        )
        for ts, row in df.iterrows()
    ]


def get_daily_snapshot(ticker: str) -> TickerDailySnapshot:
    """Get the latest daily snapshot for a given ticker."""
    prices = get_ohlcv(
        ticker=ticker,
        from_time=datetime.combine(datetime.today(), datetime.min.time()),
        to_time=datetime.now(),
        interval=Interval.min5,
    )

    current_price = prices[-1].c
    prev_close = Ticker(ticker.upper()).history(period="2d")["Close"].iloc[0]
    daily_return = round(current_price - prev_close, 2)
    daily_return_pct = round((daily_return / prev_close) * 100, 2)

    return TickerDailySnapshot(
        prices=prices,
        current_price=current_price,
        daily_return=daily_return,
        daily_return_pct=daily_return_pct,
    )
