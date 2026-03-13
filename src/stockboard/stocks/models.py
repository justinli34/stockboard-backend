from typing import ClassVar, Literal

from pydantic import BaseModel, computed_field

RangePeriod = Literal["1d", "5d", "1mo", "3mo", "ytd", "1y", "5y"]


class Range(BaseModel):
    period: Literal["1d", "5d", "1mo", "3mo", "ytd", "1y", "5y"]

    _INTERVALS: ClassVar[dict[RangePeriod, str]] = {
        "1d": "1m",
        "5d": "15m",
        "1mo": "1d",
        "3mo": "1d",
        "ytd": "1d",
        "1y": "1d",
        "5y": "1wk",
    }

    @computed_field
    @property
    def interval(self) -> str:
        return self._INTERVALS[self.period]


class OHLCV(BaseModel):
    time: str
    o: float
    h: float
    l: float  # noqa: E741
    c: float
    v: int


class Quote(BaseModel):
    current_price: float
    daily_return: float
    daily_return_pct: float


class PricePoint(BaseModel):
    time: str
    price: float
