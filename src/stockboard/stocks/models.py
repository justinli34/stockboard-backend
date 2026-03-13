from enum import Enum

from pydantic import BaseModel


class Interval(str, Enum):
    min1 = "1min"
    min5 = "5min"
    h1 = "1h"
    d1 = "1d"
    w1 = "1w"
    mo1 = "1mo"

    @property
    def yf(self) -> str:
        return {
            "1min": "1m",
            "5min": "5m",
            "1h": "1h",
            "1d": "1d",
            "1w": "1wk",
            "1mo": "1mo",
        }[self.value]


class OHLCV(BaseModel):
    t: str
    o: float
    h: float
    l: float  # noqa: E741
    c: float
    v: int


class TickerDailySnapshot(BaseModel):
    prices: list[OHLCV]
    current_price: float
    daily_return: float
    daily_return_pct: float
