from sqlalchemy import Column, Integer, String
from database import Base

class LogEntry(Base):
    __tablename__ = "logs"

    id = Column(Integer, primary_key=True, index=True)
    timestamp = Column(String, index=True)
    level = Column(String, index=True)
    service = Column(String, index=True)
    message = Column(String)
    latency_ms = Column(Integer)
    trace_id = Column(String, index=True)
