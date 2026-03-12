from fastapi import APIRouter, HTTPException, Query
from datetime import date
import yfinance as yf

router = APIRouter(prefix="/data", tags=["data"])

# Maps interval strings to yfinance-compatible intervals
INTERVAL_MAP = {
    "1m": "1m",
    "5m": "5m",
    "1h": "1h",
    "1d": "1d",
    "1w": "1wk",
    "1mo": "1mo",
}


@router.get("/{ticker}")
def get_data(
    ticker: str,
    from_date: date = Query(..., alias="from"),
    to_date: date = Query(..., alias="to"),
    interval: str = Query(...),
):
    """Get historical stock data for a given ticker and date range."""
    if interval not in INTERVAL_MAP:
        raise HTTPException(status_code=400, detail=f"Invalid interval. Choose from: {list(INTERVAL_MAP.keys())}")

    t = yf.Ticker(ticker)
    df = t.history(start=from_date, end=to_date, interval=INTERVAL_MAP[interval])

    if df.empty:
        raise HTTPException(status_code=404, detail="No data found for the given ticker and range")

    data = [
        {
            "t": int(ts.timestamp()),
            "o": round(row["Open"], 4),
            "h": round(row["High"], 4),
            "l": round(row["Low"], 4),
            "c": round(row["Close"], 4),
            "v": int(row["Volume"]),
        }
        for ts, row in df.iterrows()
    ]

    return {
        "ticker": ticker.upper(),
        "interval": interval,
        "from": str(from_date),
        "to": str(to_date),
        "data": data,
    }
