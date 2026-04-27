from sqlalchemy import create_engine, Column, Integer, String, Float, ForeignKey, DateTime
from sqlalchemy.orm import sessionmaker, DeclarativeBase, relationship
from datetime import datetime, timezone
import uuid

DATABASE_URL = "sqlite:///./stocks.db"  
connect_args = {"check_same_thread": False} if DATABASE_URL.startswith("sqlite") else {}

engine = create_engine(DATABASE_URL, connect_args=connect_args)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

class Base(DeclarativeBase):
    pass

def new_id():
    return str(uuid.uuid4())

class User(Base):
    __tablename__ = "users"

    userid = Column(String, primary_key=True, default=new_id, index=True)
    name = Column(String, index=True)
    email = Column(String, unique=True, index=True)
    hashed_pass = Column(String)

    holdings = relationship("Holding", back_populates="owner", cascade="all, delete-orphan")
    transactions = relationship("Transaction", back_populates="owner", cascade="all, delete-orphan")

class Stock(Base):
    __tablename__ = "stock_data"

    ticker = Column(String, primary_key=True, index=True) 
    name = Column(String)
    sector = Column(String, index=True)
    industry = Column(String)
    business_summary = Column(String)
    market_cap = Column(Float)
    trailing_pe = Column(Float)
    dividend_yield = Column(Float)
    last_updated = Column(DateTime, default=lambda: datetime.now(timezone.utc))

class Holding(Base):
    __tablename__ = "holdings"

    hid = Column(String, primary_key=True, default=new_id, index=True)
    userid = Column(String, ForeignKey("users.userid", ondelete="CASCADE"))
    ticker = Column(String, ForeignKey("stock_data.ticker"), index=True)
    qty = Column(Integer)
    buy_price = Column(Float)
    purchase_date = Column(DateTime, timezone=True)
    last_updated = Column(DateTime, default=lambda: datetime.now(timezone.utc))

    owner = relationship("User", back_populates="holdings")
    stock = relationship("Stock", backref="holdings")

class Transaction(Base):
    __tablename__ = "transactions"

    tid = Column(String, primary_key=True, default=new_id, index=True)
    userid = Column(String, ForeignKey("users.userid", ondelete="CASCADE"))
    ticker = Column(String, ForeignKey("stock_data.ticker"), index=True)
    type = Column(String) # 'buy' or 'sell'
    share_qty = Column(Integer)
    price = Column(Float)
    totalprice = Column(Float)
    executed_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))

    owner = relationship("User", back_populates="transactions")


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()