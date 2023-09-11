import json
import models, schemas
import pandas as pd

from datetime import date, datetime, timedelta
from typing import Union, List
from fastapi.responses import StreamingResponse
from fastapi import FastAPI, Depends, FastAPI, HTTPException
from schemas import SqlQuery
from database import SessionLocal, engine, select
from sqlalchemy.orm import Session
from sqlalchemy import between, text


app = FastAPI()


# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get("/")
def home():
    return {"message": "Fast Api app"}


@app.get("/live/katcpsensor/api/", response_model=list[schemas.KatcpSensor])
def get_sensor_values(
    sensor_name: str,
    start_date: date,
    stop_date: Union[date, None] = None,
    device: Union[str, None] = None,
    status: Union[int, None] = None,
    skip: int = 0,
    limit: Union[int, None] = None,
    db: Session = Depends(get_db),
):
    stmt = select(models.KatcpSensor)
    if start_date:
        if stop_date is None:
            stop_date = start_date + timedelta(days=1)
        stmt = stmt.where(between(models.KatcpSensor.timestamp, start_date, stop_date))
    if sensor_name:
        stmt = stmt.where(models.KatcpSensor.name == sensor_name)
    if device:
        stmt = stmt.where(models.KatcpSensor.device == device)
    if status:
        stmt = stmt.where(models.KatcpSensor.status == status)
    stmt = stmt.offset(skip).limit(limit)
    print(stmt)
    res = db.execute(stmt).scalars().fetchall()
    print(res)
    return res


@app.post("/live/katcpsensor/api/sql")
async def get_result_from_sql_query(sql: SqlQuery, db: Session = Depends(get_db)):
    res = db.execute(text(sql.query)).all()

    r = {}
    print(res)
    r["data"] = str(res)

    return json.dumps(r)


@app.get("/live/katcpsensor/api/extract/")
def get_sensor_values_csv(
    sensor_name: str,
    start_date: date,
    stop_date: Union[date, None] = None,
    device: Union[str, None] = None,
    status: Union[int, None] = None,
    skip: int = 0,
    limit: Union[int, None] = None,
    db: Session = Depends(get_db),
):
    stmt = select(models.KatcpSensor)
    if start_date:
        if stop_date is None:
            stop_date = start_date + timedelta(days=1)
        stmt = stmt.where(between(models.KatcpSensor.timestamp, start_date, stop_date))
    if sensor_name:
        stmt = stmt.where(models.KatcpSensor.name == sensor_name)
    if device:
        stmt = stmt.where(models.KatcpSensor.device == device)
    if status:
        stmt = stmt.where(models.KatcpSensor.status == status)
    stmt = stmt.offset(skip).limit(limit)
    print(stmt)
    res = db.execute(stmt).scalars().fetchall()
    df = pd.DataFrame([(r.timestamp, r.value, r.status) for r in res])
    # df.columns = ["timestamp", "value", "status"]
    print(df)
    return StreamingResponse(
        iter([df.to_csv(index=False)]),
        media_type="text/csv",
        headers={"Content-Disposition": f"attachment;filename={sensor_name}.csv"},
    )
