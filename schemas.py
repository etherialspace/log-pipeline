from pydantic import BaseModel
from typing import Optional

class LogEntryBase(BaseModel):
    timestamp: str
    level: str
    service: str
    message: str
    latency_ms: int
    trace_id: str

class LogEntryCreate(LogEntryBase):
    pass

class LogEntry(LogEntryBase):
    id: int

    class Config:
        orm_mode = True
        from_attributes = True
