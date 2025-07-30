import math

from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pydantic import BaseModel
from typing import List, Dict
import uuid
import uvicorn

app = FastAPI(title="Driver & Rider Management API", version="1.0.0")

# In-memory storage
drivers_db: Dict[str, dict] = {}
riders_db: Dict[str, dict] = {}
ride_requests_db: Dict[str, dict] = {}
time: int = 0


# Pydantic models
class Driver(BaseModel):
    id: str
    name: str
    current_x: float
    current_y: float


class DriverCreate(BaseModel):
    name: str
    current_x: float
    current_y: float


class Rider(BaseModel):
    id: str
    name: str


class RiderCreate(BaseModel):
    name: str


class RideRequest(BaseModel):
    id: str
    rider_id: str
    pickup_x: float
    pickup_y: float
    dropoff_x: float
    dropoff_y: float


class RideRequestCreate(BaseModel):
    rider_id: str
    pickup_x: float
    pickup_y: float
    dropoff_x: float
    dropoff_y: float


# Mount static files
app.mount("/static", StaticFiles(directory="static"), name="static")


@app.get("/")
async def read_root():
    return FileResponse("static/index.html")


@app.get("/drivers", response_model=List[Driver])
async def get_drivers():
    """Get all drivers"""
    return list(drivers_db.values())


@app.post("/drivers", response_model=Driver)
async def create_driver(driver: DriverCreate):
    """Create a new driver"""
    driver_id = str(uuid.uuid4())
    new_driver = {
        "id": driver_id,
        "name": driver.name,
        "current_x": driver.current_x,
        "current_y": driver.current_y
    }
    drivers_db[driver_id] = new_driver
    return new_driver


@app.get("/drivers/{driver_id}", response_model=Driver)
async def get_driver(driver_id: str):
    """Get a specific driver by ID"""
    if driver_id not in drivers_db:
        raise HTTPException(status_code=404, detail="Driver not found")
    return drivers_db[driver_id]


@app.delete("/drivers/{driver_id}")
async def delete_driver(driver_id: str):
    """Delete a driver"""
    if driver_id not in drivers_db:
        raise HTTPException(status_code=404, detail="Driver not found")
    del drivers_db[driver_id]
    return {"message": "Driver deleted successfully"}


@app.get("/riders", response_model=List[Rider])
async def get_riders():
    """Get all riders"""
    return list(riders_db.values())


@app.post("/riders", response_model=Rider)
async def create_rider(rider: RiderCreate):
    """Create a new rider"""
    rider_id = str(uuid.uuid4())
    new_rider = {
        "id": rider_id,
        "name": rider.name,
    }
    riders_db[rider_id] = new_rider
    return new_rider


@app.get("/riders/{rider_id}", response_model=Rider)
async def get_rider(rider_id: str):
    """Get a specific rider by ID"""
    if rider_id not in riders_db:
        raise HTTPException(status_code=404, detail="Rider not found")
    return riders_db[rider_id]


@app.delete("/riders/{rider_id}")
async def delete_rider(rider_id: str):
    """Delete a rider"""
    if rider_id not in riders_db:
        raise HTTPException(status_code=404, detail="Rider not found")
    del riders_db[rider_id]
    return {"message": "Rider deleted successfully"}


@app.post("/ride_requests", response_model=RideRequest)
async def create_ride_request(ride_request: RideRequestCreate):
    """Create a new ride request"""
    # Validate that the rider exists
    if ride_request.rider_id not in riders_db:
        raise HTTPException(status_code=404, detail="Rider not found")

    ride_request_id = str(uuid.uuid4())
    new_ride_request = {
        "id": ride_request_id,
        "rider_id": ride_request.rider_id,
        "pickup_x": ride_request.pickup_x,
        "pickup_y": ride_request.pickup_y,
        "dropoff_x": ride_request.dropoff_x,
        "dropoff_y": ride_request.dropoff_y
    }
    ride_requests_db[ride_request_id] = new_ride_request
    min_euclid = 1000 # above max
    closest_driver = None
    for i, driver in enumerate(drivers_db):
        dist = math.dist((driver["current_x"], driver["current_y"]), (new_ride_request["current_x"], new_ride_request["current_y"]))
        if min_euclid > dist:
            min_euclid = dist
            closest_driver = driver["id"]
    return new_ride_request


@app.get("/ride_requests", response_model=List[RideRequest])
async def get_ride_requests():
    """Get all ride requests"""
    return list(ride_requests_db.values())


@app.get("/ride_requests/{ride_request_id}", response_model=RideRequest)
async def get_ride_request(ride_request_id: str):
    """Get a specific ride request by ID"""
    if ride_request_id not in ride_requests_db:
        raise HTTPException(status_code=404, detail="Ride request not found")
    return ride_requests_db[ride_request_id]


@app.delete("/ride_requests/{ride_request_id}")
async def delete_ride_request(ride_request_id: str):
    """Delete a ride request"""
    if ride_request_id not in ride_requests_db:
        raise HTTPException(status_code=404, detail="Ride request not found")
    del ride_requests_db[ride_request_id]
    return {"message": "Ride request deleted successfully"}


@app.post("/tick")
async def tick():
    """Increment the global time variable by 1"""
    global time
    time += 1
    return {"time": time}


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)