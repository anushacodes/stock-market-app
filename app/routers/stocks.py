from datetime import datetime, timezone
from fastapi import APIRouter, HTTPException
import yfinance as yf


stock_router = APIRouter(tags=["stocks"])

# _price_cache: dict[str, dict[str, float]] = {}
# _price_cache_ts: dict[str, datetime] = {}
# _cache_ttl_seconds = 60


# def is_cache_valid(ticker: str) -> bool:
#     if ticker not in _price_cache_ts:
#         return False
#     age = datetime.now(timezone.utc) - _price_cache_ts[ticker]
#     return age.total_seconds() < _cache_ttl_seconds


# @stock_router.get("/prices/{ticker}")
# def price_today(ticker: str):
#     if is_cache_valid(ticker):
#         return _price_cache[ticker]

#     stock = yf.Ticker(ticker)
#     history = stock.history(period="1d")
#     if history.empty:
#         raise HTTPException(status_code=404, detail="Ticker not found")

#     last_close = float(history["Close"].iloc[-1])
#     data = {"ticker": ticker, "price": last_close}
#     _price_cache[ticker] = data
#     _price_cache_ts[ticker] = datetime.now(timezone.utc)
#     return data


# @stock_router.get("/prices/batch/many")
# def price_batch(tickers: str):
#     pass



@stock_router.get("/stocks/{ticker}")
def stock_price(ticker: str):
    stock = yf.Ticker(ticker.upper())
    stock_data = stock.info
    if not stock_data:
        raise HTTPException(status_code=404, detail="Ticker not found")
    return stock_data
