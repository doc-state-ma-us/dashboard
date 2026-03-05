from sqlalchemy import Column, BigInteger, Date, Integer, Text, TIMESTAMP
from sqlalchemy.sql import func
from app.models.master import Base

class RecruitmentExamTracker(Base):
    __tablename__ = "recruitment_exam_tracker"
    __table_args__ = {"schema": "doc_dashboard_phase1"}

    exam_track_id = Column(BigInteger, primary_key=True, index=True)
    unique_id = Column(Text, index=True)
    first_name = Column(Text)
    last_name = Column(Text)
    email = Column(Text, index=True)
    phone = Column(Text)
    recruiter = Column(Text)
    recruitment_cycle = Column(Text, index=True)
    exam_month = Column(Text)
    exam_year = Column(Integer, index=True)
    registration_status = Column(Text)
    exam_cycle_stage = Column(Text)
    exam_outcome_status = Column(Text)
    action = Column(Text)
    outcome = Column(Text)
    log_date = Column(Date, index=True)
    recruiter_assessment = Column(Text)
    created_at = Column(TIMESTAMP, server_default=func.now())
