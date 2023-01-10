from typing import Literal

from fastapi import Depends, FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session

from . import config, crud, database, schemas

app = FastAPI()


app.add_middleware(
    CORSMiddleware,
    allow_origins=config.settings.BACKEND_CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/api/v1/street_report", response_model=list[schemas.StreetReport])
async def get_street_report(
    order_by_room_function: schemas.RoomFunction,
    order_direction: Literal["asc", "desc"] = "desc",
    building_type: schemas.BuildingType | None = None,
    limit: int = 100,
    db: Session = Depends(database.get_db),
):
    return crud.street_report(
        db=db,
        order_by_room_function=order_by_room_function,
        order_direction=order_direction,
        building_type=building_type,
        limit=limit,
    )


@app.get("/api/v1/building_report/{building_id}", response_model=schemas.BuildingReport)
async def get_building_report_by_id(building_id: str, db: Session = Depends(database.get_db)):
    result = crud.building_report(db=db, building_id=building_id)
    if result:
        return result
    raise HTTPException(status_code=404, detail="building_id not found")
