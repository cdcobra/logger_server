from fastapi import FastAPI, Depends
from pydantic import BaseModel
import datetime
from sqlalchemy.ext.asyncio import AsyncSession
from db import get_session, init_db
from models import LogEntryModel

app = FastAPI(on_startup=[init_db])

class LogEntry(BaseModel):
    application: str
    level: str
    message: str
    name: str | None
    funcName: str | None
    lineno: int | None

@app.post("/log")
async def receive_log(entry: LogEntry, session: AsyncSession = Depends(get_session)):

    log_record = LogEntryModel(
        application=entry.application,
        level=entry.level.upper(),
        message=entry.message,
        ins_date=datetime.datetime.now(tz=datetime.timezone.utc),
        name=entry.name,
        funcName=entry.funcName,
        lineno=entry.lineno
    )
    session.add(log_record)
    await session.commit()
    return {"status": "ok"}