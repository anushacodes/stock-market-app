from datetime import datetime
from enum import Enum
from typing import Dict
from pydantic import BaseModel, ConfigDict, EmailStr


class TransactionType(str, Enum):
    buy = "buy"
    sell = "sell"


class LoginRequest(BaseModel):
    email: EmailStr
    password: str


class SignupRequest(BaseModel):
    name: str
    email: EmailStr
    password: str


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"


class UserResponse(BaseModel):
    id: int
    name: str
    email: EmailStr
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)


class HoldingBase(BaseModel):
    ticker: str
    qty: int
    avg_buy_price: float

class HoldingCreate(BaseModel):
    ticker: str

class HoldingResponse(HoldingBase):
    hid: int
    userid: int
    
    model_config = ConfigDict(from_attributes=True)

class PortfolioAnalyticsResponse(BaseModel):
    total_invested: float
    current_value: float
    unrealized_pl: float
    return_percentage: float
    sector_weights: Dict[str, str]


class TransactionCreate(BaseModel):
    ticker: str
    type: TransactionType
    quantity: int
    price: float


class TransactionResponse(BaseModel):
    id: int
    ticker: str
    type: TransactionType
    quantity: int
    price: float
    total_price: float
    executed_at: datetime

    model_config = ConfigDict(from_attributes=True)


class PortfolioSummary(BaseModel):
    total_invested: float
    current_value: float
    unrealized_pnl: float
    return_pct: float


class TransactionSummary(BaseModel):
    total_buy: float
    total_sell: float
