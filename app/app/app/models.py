from sqlalchemy import Column, Integer, String, Float, Date
from app.database import Base


class Customer(Base):
    __tablename__ = "customers"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    country = Column(String)
    currency = Column(String)


class Invoice(Base):
    __tablename__ = "invoices"

    id = Column(Integer, primary_key=True, index=True)
    invoice_number = Column(String, unique=True, nullable=False)
    customer_name = Column(String, nullable=False)
    amount = Column(Float, nullable=False)
    tax = Column(Float, default=0)
    total_amount = Column(Float, nullable=False)
    status = Column(String, default="Pending")


class Payment(Base):
    __tablename__ = "payments"

    id = Column(Integer, primary_key=True, index=True)
    customer_name = Column(String, nullable=False)
    amount = Column(Float, nullable=False)
    reference = Column(String)
    status = Column(String, default="Unmatched")


class Dispute(Base):
    __tablename__ = "disputes"

    id = Column(Integer, primary_key=True, index=True)
    invoice_number = Column(String)
    difference = Column(Float)
    reason = Column(String)
    priority = Column(String, default="Medium")
    status = Column(String, default="Open")
