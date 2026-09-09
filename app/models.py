from datetime import datetime, timezone
from decimal import Decimal
from sqlalchemy import Column, Integer, String, Numeric, DateTime, ForeignKey, Index
from sqlalchemy.orm import relationship
from app.database import Base

def utc_now():
    return datetime.now(timezone.utc)

class Wallet(Base):
    __tablename__ = "wallets"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(String(64), unique=True, index=True, nullable=False)
    balance = Column(Numeric(precision=18, scale=2), default=Decimal("0.00"), nullable=False)
    currency = Column(String(3), default="INR", nullable=False)
    created_at = Column(DateTime, default=utc_now, nullable=False)
    updated_at = Column(DateTime, default=utc_now, onupdate=utc_now, nullable=False)

    entries = relationship("LedgerEntry", back_populates="wallet")

class Transaction(Base):
    __tablename__ = "transactions"

    id = Column(Integer, primary_key=True, index=True)
    transaction_id = Column(String(64), unique=True, index=True, nullable=False)
    idempotency_key = Column(String(128), unique=True, index=True, nullable=True)
    transaction_type = Column(String(32), nullable=True)
    amount = Column(Numeric(precision=18, scale=2), nullable=False)
    currency = Column(String(3), default="INR", nullable=False)
    status = Column(String(32), default="COMPLETED", nullable=False)
    created_at = Column(DateTime, default=utc_now, nullable=False)

    entries = relationship("LedgerEntry", back_populates="transactions", cascade="all, delete-orphan")