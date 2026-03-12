from datetime import date

from fastapi import APIRouter, Query

from stockboard.data.schemas import TickerResponse
from stockboard.data.service import get_ticker_data
from stockboard.data.types import Interval

router = APIRouter(prefix="/data", tags=["data"])


@router.get("/{ticker}")
def get_ticker(
    ticker: str,
    from_date: date = Query(..., alias="from"),
    to_date: date = Query(..., alias="to"),
    interval: Interval = Query(...),
) -> TickerResponse:
    """Get historical data for a given ticker and date range."""
    return get_ticker_data(ticker, from_date, to_date, interval)
