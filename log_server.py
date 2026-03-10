from fastapi import FastAPI, Depends
from pydantic import BaseModel
from datetime import datetime
from sqlalchemy.ext.asyncio import AsyncSession
from db import get_session, init_db
from models import LogEntryModel

app = FastAPI(on_startup=[init_db])

class LogEntry(BaseModel):
    application: str
    level: str
    message: str

@app.post("/log")
async def receive_log(entry: LogEntry, session: AsyncSession = Depends(get_session)):

    log_record = LogEntryModel(
        application=entry.application,
        level=entry.level.upper(),
        message=entry.message
    )
    session.add(log_record)
    await session.commit()
    return {"status": "ok"}