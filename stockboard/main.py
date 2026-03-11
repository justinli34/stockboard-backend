from fastapi import FastAPI, HTTPException, Query
from datetime import date
import yfinance as yf

app = FastAPI()

VALID_INTERVALS = {"1m", "5m", "15m", "30m", "1h", "4h", "1d", "1w", "1mo"}

INTERVAL_MAP = {
    "1m": "1m",
    "5m": "5m",
    "15m": "15m",
    "30m": "30m",
    "1h": "1h",
    "4h": "4h",
    "1d": "1d",
    "1w": "1wk",
    "1mo": "1mo",
}


@app.get("/data/{ticker}")
def get_data(
    ticker: str,
    from_date: date = Query(..., alias="from"),
    to_date: date = Query(default_factory=date.today, alias="to"),
    interval: str = Query(...),
):
    if interval not in VALID_INTERVALS:
        raise HTTPException(status_code=400, detail=f"Invalid interval. Choose from: {VALID_INTERVALS}")

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


def main():
    import uvicorn

    uvicorn.run("__main__:app", host="127.0.0.1", port=8000, reload=True)


if __name__ == "__main__":
    main()
