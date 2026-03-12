from stockboard.exceptions import StockBoardException


class RateLimitError(StockBoardException):
    def __init__(self, message="Rate limit exceeded. Please try again later."):
        super().__init__(message)


class NoDataError(StockBoardException):
    def __init__(self, message="No data found for the requested resource."):
        super().__init__(message)
