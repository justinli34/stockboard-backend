from stockboard.exceptions import StockBoardException


class RateLimitError(StockBoardException):
    pass


class NoDataError(StockBoardException):
    pass
