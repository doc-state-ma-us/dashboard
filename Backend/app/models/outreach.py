from sqlalchemy import Column, BigInteger, Date, Integer, Text, TIMESTAMP
from sqlalchemy.sql import func
from app.models.master import Base

class DailyOutreachLog(Base):
    __tablename__ = "daily_outreach_log"
    __table_args__ = {"schema": "doc_dashboard_phase1"}

    outreach_id = Column(BigInteger, primary_key=True, index=True)
    unique_id = Column(Text, index=True)
    first_name = Column(Text)
    last_name = Column(Text)
    email = Column(Text, index=True)
    phone = Column(Text)
    recruiter = Column(Text)
    recruitment_cycle = Column(Text, index=True)
    cycle_stage = Column(Text)
    action = Column(Text)
    num_actions = Column(Integer)
    outcome = Column(Text)
    log_date = Column(Date, index=True)
    recruiter_assessment = Column(Text)
    material_sent = Column(Text)
    created_at = Column(TIMESTAMP, server_default=func.now())
