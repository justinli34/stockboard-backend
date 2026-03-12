import uvicorn
from fastapi import FastAPI

from stockboard.data.router import router as data_router

app = FastAPI(title="StockBoard", description="Stock data API", version="0.1.0")
app.include_router(data_router)


def main():
    uvicorn.run("stockboard.main:app", host="127.0.0.1", port=8000, reload=True)


if __name__ == "__main__":
    main()
