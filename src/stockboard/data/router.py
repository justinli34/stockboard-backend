from datetime import date

import yfinance as yf
from fastapi import APIRouter, HTTPException, Query

from stockboard.data.schemas import TickerResponse
from stockboard.data.types import OHLCV, Interval

router = APIRouter(prefix="/data", tags=["data"])


@router.get("/{ticker}", response_model=TickerResponse)
def get_ticker(
    ticker: str,
    from_date: date = Query(..., alias="from"),
    to_date: date = Query(..., alias="to"),
    interval: Interval = Query(...),
) -> TickerResponse:
    """Get historical data for a given ticker and date range."""
    t = yf.Ticker(ticker.upper())
    df = t.history(start=from_date, end=to_date, interval=interval.yf)

    if df.empty:
        raise HTTPException(status_code=404, detail="No data found for the given ticker and range")

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
