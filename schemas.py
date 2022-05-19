from typing import Optional
from pydantic import BaseModel

class Customer(BaseModel):
    customerId: int
    customerFName: str
    customerLName: str
    customerEmail: str
    customerPassword: str
    customerStreet: str
    customerCity: str
    customerState: str
    customerZipcode: str