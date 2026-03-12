from datetime import date, timedelta
from zoneinfo import ZoneInfo

from yfinance import Ticker
from yfinance import exceptions as yf_exceptions

from stockboard.data.exceptions import NoDataError, RateLimitError
from stockboard.data.models import OHLCV, Interval, TickerDailySnapshot


def get_ohlcv(
    ticker: str,
    from_date: date,
    to_date: date,
    interval: Interval,
) -> list[OHLCV]:
    """Get historical data for a given ticker and date range."""
    t = Ticker(ticker.upper())

    try:
        df = t.history(start=from_date, end=to_date, interval=interval.yf)
    except yf_exceptions.YFRateLimitError:
        raise RateLimitError()
    except Exception:
        raise Exception("Error fetching historical data")

    if df.empty:
        raise NoDataError("No data found. Please check the ticker and date range.")

    return [
        OHLCV(
            t=ts.astimezone(ZoneInfo("America/New_York")).isoformat(),
            o=round(row["Open"], 4),
            h=round(row["High"], 4),
            l=round(row["Low"], 4),
            c=round(row["Close"], 4),
            v=int(row["Volume"]),
        )
        for ts, row in df.iterrows()
    ]


def get_daily_snapshot(ticker: str) -> TickerDailySnapshot:
    """Get the latest daily snapshot for a given ticker."""
    prices = get_ohlcv(
        ticker=ticker,
        from_date=date.today(),
        to_date=date.today() + timedelta(days=1, minutes=5),
        interval=Interval.min5,
    )
    current_price = prices[-1].c
    daily_return = current_price - prices[0].o
    daily_return_pct = (daily_return / prices[0].o) * 100
    return TickerDailySnapshot(
        prices=prices,
        current_price=current_price,
        daily_return=daily_return,
        daily_return_pct=daily_return_pct,
    )
