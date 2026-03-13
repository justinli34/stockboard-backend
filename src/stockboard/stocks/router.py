from datetime import datetime

from fastapi import APIRouter, Query

from stockboard.stocks.models import OHLCV, Interval, TickerDailySnapshot
from stockboard.stocks.service import get_daily_snapshot, get_ohlcv

router = APIRouter(prefix="/stocks", tags=["stocks"])


@router.get("/{ticker}/ohlcv")
def get_ticker_ohlcv(
    ticker: str,
    from_time: datetime = Query(..., alias="from"),
    to_time: datetime = Query(..., alias="to"),
    interval: Interval = Query(...),
) -> list[OHLCV]:
    """Get OHLCV data for a given ticker and date range."""
    return get_ohlcv(ticker, from_time, to_time, interval)


@router.get("/{ticker}/daily-snapshot")
def get_ticker_daily_snapshot(
    ticker: str,
) -> TickerDailySnapshot:
    """Get the latest daily snapshot for a given ticker."""
    return get_daily_snapshot(ticker)
