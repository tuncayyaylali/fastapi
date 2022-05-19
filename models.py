from database import Base
from sqlalchemy import Column, String, Integer, Float


class Customer(Base):
    __tablename__ = "customers"

    customerId = Column(Integer, primary_key=True)
    customerFName = Column(String(50))
    customerLName = Column(String(50))
    customerEmail = Column(String(50))
    customerPassword = Column(String(50))
    customerStreet = Column(String(50))
    customerCity = Column(String(50))
    customerState = Column(String(50))
    customerZipcode = Column(String(50))