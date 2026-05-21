from fastapi import FastAPI, Depends, Query
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from typing import List, Optional

import models
import schemas
from database import SessionLocal, engine

models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="Log Ingestion API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.post("/logs/", response_model=schemas.LogEntry)
def create_log(log: schemas.LogEntryCreate, db: Session = Depends(get_db)):
    db_log = models.LogEntry(**log.dict())
    db.add(db_log)
    db.commit()
    db.refresh(db_log)
    return db_log

@app.get("/logs/", response_model=List[schemas.LogEntry])
def read_logs(
    skip: int = 0,
    limit: int = 100,
    level: Optional[str] = None,
    service: Optional[str] = None,
    db: Session = Depends(get_db)
):
    query = db.query(models.LogEntry)
    if level:
        query = query.filter(models.LogEntry.level == level)
    if service:
        query = query.filter(models.LogEntry.service == service)
        
    logs = query.offset(skip).limit(limit).all()
    return logs
