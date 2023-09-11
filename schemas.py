from pydantic import BaseModel
from datetime import datetime


class SqlQuery(BaseModel):
    description: str | None = None
    query: str


class KatcpSensorResponse(BaseModel):
    name: str
    data: list


class KatcpSensor(BaseModel):
    id: int
    timestamp: datetime
    device: str
    name: str
    status: int
    value: str

    class Config:
        from_attributes = True
