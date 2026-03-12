from datetime import date

from pydantic import BaseModel, Field

from stockboard.data.types import OHLCV, Interval


class TickerResponse(BaseModel):
    ticker: str
    interval: Interval
    from_date: date = Field(serialization_alias="from")
    to_date: date = Field(serialization_alias="to")
    data: list[OHLCV]
