from fastapi import HTTPException, status

EmailExists = HTTPException(status_code=400, detail="User email already exists")
UsernameExists = HTTPException(status_code=400, detail="Username already exists")
VisitNotFound = HTTPException(status_code=404, detail="Visit not found")
ServiceNotFound = HTTPException(status_code=404, detail="Service not found")
WorkerNotFound = HTTPException(status_code=404, detail="Worker not found")
WorkerNotSkilled = HTTPException(
    status_code=404, detail="Worker not skilled of a service"
)
SlotNotAvailable = HTTPException(status_code=409, detail="Slot is not availiable")
SlotType = HTTPException(status_code=400, detail=f"Wrong slot type")

BadCreds = HTTPException(status_code=400, detail="Incorrect username or password")
BadToken = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail="Bad token!!!",
    headers={"WWW-Authenticate": "Bearer"},
)
