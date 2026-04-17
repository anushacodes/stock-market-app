# Stock Portfolio Watcher

Stock Portfolio Watcher is a FastAPI backend for tracking a personal stock portfolio. It lets users register, track holdings, log buy/sell transactions, fetch live prices with yfinance, and view simple portfolio analytics.



## Tech Stack

* FastAPI
* SQLAlchemy 
* SQLite (dev) / Postgres
* JWT Authentication
* yfinance (price data)
* Jinja2 template


## Features

### Authentication

* Register a new user
* Login and receive JWT token
* Access protected routes

### User

* Retrieve current user profile

### Holdings

* Add a ticker to track
* View all holdings
* Remove a holding (qty = 0)

### Transactions

* Log buy/sell transactions
* View transaction history 
* Automatically update holdings

### Prices

* Fetch live stock prices (yfinance)
* Batch fetch multiple tickers
* In-memory caching to reduce API calls (future)

### Analytics

* Portfolio-level P&L (unrealized gains/losses)
* Transaction summaries (buy vs sell totals)
* News based predictions (future improvement)

---

## API Endpoints

| Method | Endpoint                                   | Description                  |
| ------ | ------------------------------------------ | ---------------------------- |
| POST   | `/auth/register`                           | Register user                |
| POST   | `/auth/login`                              | Login and get token          |
| GET    | `/users/me`                                | Current user profile         |
| GET    | `/portfolio`                               | List holdings                |
| POST   | `/portfolio/holdings`                      | Add holding                  |
| DELETE | `/portfolio/holdings/{holding_id}`         | Delete holding               |
| GET    | `/transactions`                            | Transaction history          |
| POST   | `/transactions`                            | Create transaction           |
| GET    | `/prices/{ticker}`                         | Get current price            |
| GET    | `/prices/batch/many?tickers=AAPL,MSFT`      | Batch prices                 |
| GET    | `/portfolio/analytics`                     | Portfolio P&L                |
| GET    | `/portfolio/analytics/transactions-summary`| Transaction summary          |
| GET    | `/stocks/{ticker}`                         | Company info                 |

---

## Database Schema (current)

### users

* id (uuid)
* name
* email
* password_hash
* created_at

### holdings

* hid (uuid)
* user_id (FK)
* ticker
* quantity
* avg_buy_price
* created_at
* updated_at

### transactions

* tid (int)
* user_id (FK)
* ticker
* type (buy/sell)
* quantity
* price
* total_price
* executed_at

---

## Project Structure

```
app/
    main.py
    config.py
    database.py
    dependencies.py
    security.py
    routers/
        user.py
        portfolio.py
        transactions.py
        stocks.py
  schemas.py
  static/
  templates/
```


## Frontend

* `/` landing page (public price lookup)
* `/login` and `/register`
* `/dashboard` uses API endpoints and JWT stored in localStorage