from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.schema import Table
from db import Base, SCHEMA_NAME
import datetime

class LogEntryModel(Base):
    __tablename__ = "logs"
    __table_args__ = {"schema": SCHEMA_NAME}

    id = Column(Integer, primary_key=True, index=True)
    ins_date = Column(DateTime(timezone=True), nullable=False, default=datetime.datetime.now(tz=datetime.timezone.utc))
    application = Column(String, nullable=False)
    level = Column(String, nullable=False)
    message = Column(String, nullable=False)