import uvicorn
from fastapi import FastAPI
from fastapi.responses import JSONResponse

from stockboard.data.exceptions import NoDataError, RateLimitError
from stockboard.data.router import router as data_router
from stockboard.exceptions import StockBoardException

app = FastAPI(title="StockBoard", description="Stock data API", version="0.1.0")
app.include_router(data_router)


@app.exception_handler(StockBoardException)
def stockboard_exception_handler(request, e):
    match e:
        case NoDataError():
            status = 404
            detail = str(e)
        case RateLimitError():
            status = 429
            detail = str(e)
        case _:
            status = 500
            detail = "An unexpected error occurred. Please try again later."
    return JSONResponse(status_code=status, content={"detail": detail})


def main():
    uvicorn.run("stockboard.main:app", host="127.0.0.1", port=8000, reload=True)


if __name__ == "__main__":
    main()
