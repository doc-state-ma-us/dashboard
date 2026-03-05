#dashboard_service.py
from sqlalchemy.orm import Session
from sqlalchemy import func
from datetime import date

from app.models.master import Master
from app.models.outreach import DailyOutreachLog
from app.models.exam_tracker import RecruitmentExamTracker


def master_stats(db: Session, start_date: date, end_date: date):
    base = (
        db.query(Master)
        .filter(Master.submission_date >= start_date)
        .filter(Master.submission_date <= end_date)
    )

    # KPI: New candidates (dedupe by email)
    new_candidates = (
        db.query(func.count(func.distinct(Master.email)))
        .filter(Master.submission_date >= start_date)
        .filter(Master.submission_date <= end_date)
        .scalar()
    ) or 0

    # Bar: Source counts (dedupe by email)
    source_rows = (
        db.query(Master.source, func.count(func.distinct(Master.email)))
        .filter(Master.submission_date >= start_date)
        .filter(Master.submission_date <= end_date)
        .group_by(Master.source)
        .order_by(func.count(func.distinct(Master.email)).desc())
        .all()
    )
    source_chart = [{"label": (s or "Unknown"), "value": int(c)} for s, c in source_rows]

    # Donut: Recruiter assigned (dedupe by email)
    recruiter_rows = (
        db.query(Master.recruiter, func.count(func.distinct(Master.email)))
        .filter(Master.submission_date >= start_date)
        .filter(Master.submission_date <= end_date)
        .group_by(Master.recruiter)
        .order_by(func.count(func.distinct(Master.email)).desc())
        .all()
    )
    recruiter_chart = [{"label": (r or "Unassigned"), "value": int(c)} for r, c in recruiter_rows]

    return {
        "range": {"start_date": str(start_date), "end_date": str(end_date)},
        "kpis": {"new_candidates": int(new_candidates)},
        "charts": {
            "source_bar": source_chart,
            "recruiter_donut": recruiter_chart
        }
    }


def outreach_stats(db: Session, start_date: date, end_date: date):
    # Bar: cycle_stage
    cycle_stage_rows = (
        db.query(DailyOutreachLog.cycle_stage, func.count())
        .filter(DailyOutreachLog.log_date >= start_date)
        .filter(DailyOutreachLog.log_date <= end_date)
        .group_by(DailyOutreachLog.cycle_stage)
        .order_by(func.count().desc())
        .all()
    )
    cycle_stage_chart = [{"label": (x or "Unknown"), "value": int(c)} for x, c in cycle_stage_rows]

    # Pie: action
    action_rows = (
        db.query(DailyOutreachLog.action, func.count())
        .filter(DailyOutreachLog.log_date >= start_date)
        .filter(DailyOutreachLog.log_date <= end_date)
        .group_by(DailyOutreachLog.action)
        .order_by(func.count().desc())
        .all()
    )
    action_pie = [{"label": (a or "Unknown"), "value": int(c)} for a, c in action_rows]

    # KPI: total actions taken (sum num_actions)
    total_actions = (
        db.query(func.coalesce(func.sum(DailyOutreachLog.num_actions), 0))
        .filter(DailyOutreachLog.log_date >= start_date)
        .filter(DailyOutreachLog.log_date <= end_date)
        .scalar()
    ) or 0

    # Bar: outcome
    outcome_rows = (
        db.query(DailyOutreachLog.outcome, func.count())
        .filter(DailyOutreachLog.log_date >= start_date)
        .filter(DailyOutreachLog.log_date <= end_date)
        .group_by(DailyOutreachLog.outcome)
        .order_by(func.count().desc())
        .all()
    )
    outcome_chart = [{"label": (o or "Unknown"), "value": int(c)} for o, c in outcome_rows]

    # Bar: recruiter_assessment
    assessment_rows = (
        db.query(DailyOutreachLog.recruiter_assessment, func.count())
        .filter(DailyOutreachLog.log_date >= start_date)
        .filter(DailyOutreachLog.log_date <= end_date)
        .group_by(DailyOutreachLog.recruiter_assessment)
        .order_by(func.count().desc())
        .all()
    )
    assessment_chart = [{"label": (a or "Unknown"), "value": int(c)} for a, c in assessment_rows]

    return {
        "range": {"start_date": str(start_date), "end_date": str(end_date)},
        "kpis": {"total_actions_taken": int(total_actions)},
        "charts": {
            "cycle_stage_bar": cycle_stage_chart,
            "action_pie": action_pie,
            "outcome_bar": outcome_chart,
            "recruiter_assessment_bar": assessment_chart,
        }
    }


def exam_stats(db: Session, start_date: date, end_date: date):
    # Bar: exam_cycle_stage
    stage_rows = (
        db.query(RecruitmentExamTracker.exam_cycle_stage, func.count())
        .filter(RecruitmentExamTracker.log_date >= start_date)
        .filter(RecruitmentExamTracker.log_date <= end_date)
        .group_by(RecruitmentExamTracker.exam_cycle_stage)
        .order_by(func.count().desc())
        .all()
    )
    stage_chart = [{"label": (s or "Unknown"), "value": int(c)} for s, c in stage_rows]

    # Pie: action
    action_rows = (
        db.query(RecruitmentExamTracker.action, func.count())
        .filter(RecruitmentExamTracker.log_date >= start_date)
        .filter(RecruitmentExamTracker.log_date <= end_date)
        .group_by(RecruitmentExamTracker.action)
        .order_by(func.count().desc())
        .all()
    )
    action_pie = [{"label": (a or "Unknown"), "value": int(c)} for a, c in action_rows]

    # Bar: outcome
    outcome_rows = (
        db.query(RecruitmentExamTracker.outcome, func.count())
        .filter(RecruitmentExamTracker.log_date >= start_date)
        .filter(RecruitmentExamTracker.log_date <= end_date)
        .group_by(RecruitmentExamTracker.outcome)
        .order_by(func.count().desc())
        .all()
    )
    outcome_chart = [{"label": (o or "Unknown"), "value": int(c)} for o, c in outcome_rows]

    # Bar: recruiter_assessment
    assessment_rows = (
        db.query(RecruitmentExamTracker.recruiter_assessment, func.count())
        .filter(RecruitmentExamTracker.log_date >= start_date)
        .filter(RecruitmentExamTracker.log_date <= end_date)
        .group_by(RecruitmentExamTracker.recruiter_assessment)
        .order_by(func.count().desc())
        .all()
    )
    assessment_chart = [{"label": (a or "Unknown"), "value": int(c)} for a, c in assessment_rows]

    # Donut: recruiter contribution
    recruiter_rows = (
        db.query(RecruitmentExamTracker.recruiter, func.count())
        .filter(RecruitmentExamTracker.log_date >= start_date)
        .filter(RecruitmentExamTracker.log_date <= end_date)
        .group_by(RecruitmentExamTracker.recruiter)
        .order_by(func.count().desc())
        .all()
    )
    recruiter_donut = [{"label": (r or "Unassigned"), "value": int(c)} for r, c in recruiter_rows]

    return {
        "range": {"start_date": str(start_date), "end_date": str(end_date)},
        "kpis": {},
        "charts": {
            "exam_cycle_stage_bar": stage_chart,
            "action_pie": action_pie,
            "outcome_bar": outcome_chart,
            "recruiter_assessment_bar": assessment_chart,
            "recruiter_donut": recruiter_donut,
        }
    }
