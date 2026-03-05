from sqlalchemy import Column, Date, Text, TIMESTAMP
from sqlalchemy.sql import func
from sqlalchemy.orm import declarative_base

Base = declarative_base()

class Master(Base):
    __tablename__ = "master"
    __table_args__ = {"schema": "doc_dashboard_phase1"}

    unique_id = Column(Text, primary_key=True, index=True)
    submission_date = Column(Date)
    first_name = Column(Text)
    last_name = Column(Text)
    email = Column(Text, index=True)
    phone = Column(Text)
    city = Column(Text)
    state = Column(Text)
    source = Column(Text)
    recruiter = Column(Text)
    recruitment_cycle = Column(Text, index=True)
    created_at = Column(TIMESTAMP, server_default=func.now())
