from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional
from uuid import uuid4

app = FastAPI(title="Mashinalar API")

# --- CORS sozlamalari ---
origins = ["*"]  # barcha domenlarga ruxsat beriladi, real loyihada faqat frontend domenini qo'yish kerak
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mashina modeli
class Car(BaseModel):
    id: Optional[str] = None
    brand: str
    model: str
    year: int
    color: str
    image_url: Optional[str] = None  # rasm link sifatida

# In-memory ma'lumotlar saqlash
cars_db: List[Car] = []

# CREATE: Yangi mashina
@app.post("/cars/", response_model=Car)
def create_car(car: Car):
    car.id = str(uuid4())  # unikal ID
    cars_db.append(car)
    return car

# READ: Barcha mashinalar
@app.get("/cars/", response_model=List[Car])
def get_cars():
    return cars_db

# READ: ID bo'yicha mashina
@app.get("/cars/{car_id}", response_model=Car)
def get_car(car_id: str):
    for car in cars_db:
        if car.id == car_id:
            return car
    raise HTTPException(status_code=404, detail="Mashina topilmadi")

# UPDATE: Mashina ma'lumotlarini yangilash
@app.put("/cars/{car_id}", response_model=Car)
def update_car(car_id: str, updated_car: Car):
    for index, car in enumerate(cars_db):
        if car.id == car_id:
            updated_car.id = car_id
            cars_db[index] = updated_car
            return updated_car
    raise HTTPException(status_code=404, detail="Mashina topilmadi")

# DELETE: Mashinani o'chirish
@app.delete("/cars/{car_id}", response_model=dict)
def delete_car(car_id: str):
    for index, car in enumerate(cars_db):
        if car.id == car_id:
            cars_db.pop(index)
            return {"message": "Mashina o'chirildi"}
    raise HTTPException(status_code=404, detail="Mashina topilmadi")
