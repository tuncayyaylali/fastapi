from fastapi import FastAPI, status, HTTPException, Response
import schemas
from typing import Optional
import models
from database import engine, get_db
from sqlalchemy.orm import Session
from fastapi import Depends
from http import HTTPStatus

app = FastAPI()

models.Base.metadata.create_all(bind=engine)

# Query parameters
@app.get("/customers")
async def get_customer(db: Session = Depends(get_db)):
    customers = db.query(models.Customer).all()
    return customers
    
# Get customer by id
@app.get("/customers/{id}")
async def get_customer_by_id(id: int, db: Session = Depends(get_db)):
    customer = db.query(models.Customer).filter(models.Customer.customerId == id).first()
    if not customer:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Customer ID: {id} has not found.")
    return customer

# Get customer by city
@app.get("/customers/{city}/limit")
async def get_customer_by_city(city: str, limit: int = 10, db: Session = Depends(get_db)):
    customers = db.query(models.Customer).all()
    
    customers_return = []
    for cust in customers:
        if cust.customerCity == city:
            customers_return.append(cust)
    return customers_return[:limit]
       
# Create customer
@app.post("/customers",  status_code=status.HTTP_201_CREATED)
async def create_customer(request: schemas.Customer, db: Session = Depends(get_db)):
    new_customer = models.Customer(
        customerId=request.customerId,
        customerFName=request.customerFName,
        customerLName=request.customerLName,
        customerEmail=request.customerEmail,
        customerPassword=request.customerPassword,
        customerStreet=request.customerStreet,
        customerCity=request.customerCity,
        customerState=request.customerState,
        customerZipcode=request.customerZipcode
        )

    db.add(new_customer)
    db.commit()
    db.refresh(new_customer)
    return new_customer

# Update customer
@app.put("/customer/{id}", status_code=status.HTTP_202_ACCEPTED)
async def update_customer_by_id(id: int, request: schemas.Customer, db: Session = Depends(get_db)):
    customer = db.query(models.Customer).filter(models.Customer.customerId == id)
    if not customer.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Customer ID: {id} has not found.")

    customer.update(request.dict(), synchronize_session=False)
    db.commit()
    return {"detail": f"Customer {id} is updated."}

# Delete a customer
@app.delete("/customer/{id}", status_code=HTTPStatus.NO_CONTENT)
async def delete_customer_by_id(id: int, db: Session = Depends(get_db)):
    customer = db.query(models.Customer).filter(models.Customer.customerId == id)
    if not customer.first():
      raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail=f"Customer {id} has not found.")      
    customer.delete(synchronize_session=False)    
    db.commit()
    return Response(status_code=HTTPStatus.NO_CONTENT.value)