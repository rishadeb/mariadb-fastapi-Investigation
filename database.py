from sqlalchemy import create_engine
from sqlalchemy import URL
from sqlalchemy import select
from sqlalchemy.orm import Session, sessionmaker
from models import KatcpSensor

url_object = URL.create(
    "mysql+mysqlconnector",
    username="user2",
    password="password1",
    host="127.0.0.1",
    database="database",
)
engine = create_engine(url_object, echo=True)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# session = Session(engine)

# stmt = select(KatcpSensor.timestamp, KatcpSensor.value, KatcpSensor.status).where(KatcpSensor.name == "acs.mode")
# print(stmt)
# res = session.execute(stmt)
# print([(str(h), i, j) for (h,i,j) in res])
