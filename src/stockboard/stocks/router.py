from fastapi import APIRouter, Query

from stockboard.stocks.models import OHLCV, PricePoint, Quote, Range, RangePeriod
from stockboard.stocks.service import fetch_ohlcv, fetch_preview_data, fetch_quote

router = APIRouter(prefix="/stocks", tags=["stocks"])


@router.get("/ohlcv")
def get_ohlcv(
    tickers: list[str] = Query(..., alias="tickers"),
    range: RangePeriod = Query(..., alias="range"),
) -> dict[str, list[OHLCV]]:
    """Get OHLCV data for the given tickers and time range."""
    return {ticker: fetch_ohlcv(ticker, Range(period=range)) for ticker in tickers}


@router.get("/quotes")
def get_quotes(
    tickers: list[str] = Query(..., alias="tickers"),
) -> dict[str, Quote]:
    """Get daily quotes for the given tickers."""
    return {ticker: fetch_quote(ticker) for ticker in tickers}


@router.get("/preview-data")
def get_preview_data(
    tickers: list[str] = Query(..., alias="tickers"),
) -> dict[str, list[PricePoint]]:
    """Get preview data for the given tickers."""
    return {ticker: fetch_preview_data(ticker) for ticker in tickers}
