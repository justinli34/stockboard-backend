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
        case RateLimitError():
            status = 429
    return JSONResponse(status_code=status, content={"detail": str(e)})


@app.exception_handler(Exception)
def generic_exception_handler(request, e):
    return JSONResponse(status_code=500, content={"detail": "An unexpected error occurred. Please try again later."})


def main():
    uvicorn.run("stockboard.main:app", host="127.0.0.1", port=8000, reload=True)


if __name__ == "__main__":
    main()
