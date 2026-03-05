from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from datetime import date
from app.db.session import get_db
from app.services.dashboard_service import (
    master_stats,
    outreach_stats,
    exam_stats
)

router = APIRouter(prefix="/dashboard", tags=["Dashboard"])

@router.get("/master")
def get_master_dashboard(
    start_date: date = Query(...),
    end_date: date = Query(...),
    db: Session = Depends(get_db),
):
    return master_stats(db, start_date, end_date)

@router.get("/outreach")
def get_outreach_dashboard(
    start_date: date = Query(...),
    end_date: date = Query(...),
    db: Session = Depends(get_db),
):
    return outreach_stats(db, start_date, end_date)

@router.get("/exam")
def get_exam_dashboard(
    start_date: date = Query(...),
    end_date: date = Query(...),
    db: Session = Depends(get_db),
):
    return exam_stats(db, start_date, end_date)
