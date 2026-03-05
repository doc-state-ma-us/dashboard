import pandas as pd
from sqlalchemy import create_engine, text

DB_CONFIG = {
    "dbname": "Dashboard_phase2",
    "user": "postgres",
    "password": "atsdatabase",
    "host": "localhost",
    "port": 5432
}

EXCEL_PATH = r"Recruitment DatabaseFeb-27.xlsx"   # <-- CHANGE THIS

# -----------------------------
# Helpers: shared transformations
# -----------------------------
def clean_text_series(s: pd.Series) -> pd.Series:
    s = s.astype("string")
    s = s.str.replace(r"\s+", " ", regex=True).str.strip()
    s = s.replace("", pd.NA)
    return s

def clean_email(s: pd.Series) -> pd.Series:
    s = clean_text_series(s)
    return s.str.lower()

def clean_phone(s: pd.Series) -> pd.Series:
    s = clean_text_series(s)
    s = s.str.replace(r"\D+", "", regex=True)     # digits only
    s = s.where(s.str.len() >= 7, pd.NA)          # optional sanity check
    return s

def clean_state(s: pd.Series) -> pd.Series:
    s = clean_text_series(s)
    return s.str.upper()

def clean_date(s: pd.Series) -> pd.Series:
    dt = pd.to_datetime(s, errors="coerce")
    return dt.dt.date

def apply_common_transforms(df: pd.DataFrame) -> pd.DataFrame:
    if "email" in df.columns:
        df["email"] = clean_email(df["email"])
    if "phone" in df.columns:
        df["phone"] = clean_phone(df["phone"])

    for col in [
        "city", "state", "source", "first_name", "last_name", "recruiter", "recruitment_cycle",
        "cycle_stage", "action", "outcome", "recruiter_assessment", "material_sent",
        "exam_month", "registration_status", "exam_cycle_stage", "exam_outcome_status"
    ]:
        if col in df.columns:
            df[col] = clean_text_series(df[col])

    if "state" in df.columns:
        df["state"] = clean_state(df["state"])

    return df

# -----------------------------
# Column selection (ONLY your columns)
# -----------------------------
MASTER_COLS = [
    "Unique ID", "Submission Date", "First Name", "Last Name", "Email", "Phone",
    "City", "State", "Source", "Recruiter", "Recruitment Cycle"
]

OUTREACH_COLS = [
    "Unique ID", "First Name", "Last Name", "Email", "Phone", "Recruiter",
    "Recruitment Cycle", "Cycle Stage", "Action", "# of actions", "Outcome",
    "Log Date", "Recruiter Assessment", "Material Sent"
]

EXAM_COLS = [
    "Unique ID", "First Name", "Last Name", "Email", "Phone", "Recruiter",
    "Recruitment Cycle", "Exam Month", "Exam Year", "Registration Status",
    "Exam Cycle Stage", "Exam outcome/ Status", "Action", "Outcome", "Log Date",
    "Recruiter Assessment"
]

def standardize_columns(df: pd.DataFrame) -> pd.DataFrame:
    rename_map = {
        "Unique ID": "unique_id",
        "Submission Date": "submission_date",
        "First Name": "first_name",
        "Last Name": "last_name",
        "Email": "email",
        "Phone": "phone",
        "City": "city",
        "State": "state",
        "Source": "source",
        "Recruiter": "recruiter",
        "Recruitment Cycle": "recruitment_cycle",
        "Cycle Stage": "cycle_stage",
        "Action": "action",
        "# of actions": "num_actions",
        "Outcome": "outcome",
        "Log Date": "log_date",
        "Recruiter Assessment": "recruiter_assessment",
        "Material Sent": "material_sent",
        "Exam Month": "exam_month",
        "Exam Year": "exam_year",
        "Registration Status": "registration_status",
        "Exam Cycle Stage": "exam_cycle_stage",
        "Exam outcome/ Status": "exam_outcome_status",
    }
    return df.rename(columns=rename_map)

def read_sheet_selected(path: str, sheet_name: str, cols: list[str]) -> pd.DataFrame:
    df = pd.read_excel(path, sheet_name=sheet_name, engine="openpyxl")
    df = df.loc[:, [c for c in cols if c in df.columns]]
    return df

def build_engine():
    conn_str = (
        f"postgresql+psycopg2://{DB_CONFIG['user']}:{DB_CONFIG['password']}"
        f"@{DB_CONFIG['host']}:{DB_CONFIG['port']}/{DB_CONFIG['dbname']}"
    )
    return create_engine(conn_str)

def main():
    engine = build_engine()

    # -----------------------------
    # Extract
    # -----------------------------
    master = read_sheet_selected(EXCEL_PATH, "Master", MASTER_COLS)
    outreach = read_sheet_selected(EXCEL_PATH, "Daily Outreach Log", OUTREACH_COLS)
    exam = read_sheet_selected(EXCEL_PATH, "Recruitment Exam Tracker", EXAM_COLS)

    # -----------------------------
    # Transform
    # -----------------------------
    master = apply_common_transforms(standardize_columns(master))
    outreach = apply_common_transforms(standardize_columns(outreach))
    exam = apply_common_transforms(standardize_columns(exam))

    # Dates
    if "submission_date" in master.columns:
        master["submission_date"] = clean_date(master["submission_date"])
    if "log_date" in outreach.columns:
        outreach["log_date"] = clean_date(outreach["log_date"])
    if "log_date" in exam.columns:
        exam["log_date"] = clean_date(exam["log_date"])

    # Numbers
    if "num_actions" in outreach.columns:
        outreach["num_actions"] = pd.to_numeric(outreach["num_actions"], errors="coerce").astype("Int64")
    if "exam_year" in exam.columns:
        exam["exam_year"] = pd.to_numeric(exam["exam_year"], errors="coerce").astype("Int64")

    # Drop blanks
    master = master[master["unique_id"].notna()]
    outreach = outreach[outreach["unique_id"].notna()]
    exam = exam[exam["unique_id"].notna()]

    # -----------------------------
    # Load (single transaction)
    # -----------------------------
    with engine.begin() as conn:
        # 1) Master UPSERT using staging table
        staging_table = "stg_master"
        # Replace staging each run
        master.to_sql(staging_table, conn, schema="doc_dashboard_phase1", if_exists="replace", index=False)

        upsert_sql = """
        INSERT INTO doc_dashboard_phase1.master (
            unique_id, submission_date, first_name, last_name, email, phone,
            city, state, source, recruiter, recruitment_cycle
        )
        SELECT
            unique_id, submission_date, first_name, last_name, email, phone,
            city, state, source, recruiter, recruitment_cycle
        FROM doc_dashboard_phase1.stg_master
        WHERE unique_id IS NOT NULL
        ON CONFLICT (unique_id) DO UPDATE SET
            submission_date   = EXCLUDED.submission_date,
            first_name        = EXCLUDED.first_name,
            last_name         = EXCLUDED.last_name,
            email             = EXCLUDED.email,
            phone             = EXCLUDED.phone,
            city              = EXCLUDED.city,
            state             = EXCLUDED.state,
            source            = EXCLUDED.source,
            recruiter         = EXCLUDED.recruiter,
            recruitment_cycle = EXCLUDED.recruitment_cycle;
        """
        conn.execute(text(upsert_sql))

        # Optional: drop staging (nice & clean)
        conn.execute(text("DROP TABLE IF EXISTS doc_dashboard_phase1.stg_master;"))

        # 2) Outreach + Exam Tracker: TRUNCATE + reload
        conn.execute(text("TRUNCATE TABLE doc_dashboard_phase1.daily_outreach_log;"))
        conn.execute(text("TRUNCATE TABLE doc_dashboard_phase1.recruitment_exam_tracker;"))

        outreach.to_sql("daily_outreach_log", conn, schema="doc_dashboard_phase1", if_exists="append", index=False)
        exam.to_sql("recruitment_exam_tracker", conn, schema="doc_dashboard_phase1", if_exists="append", index=False)

    print("✅ Weekly ETL done: Master UPSERT + Outreach/Exam TRUNCATE & reload completed.")

if __name__ == "__main__":
    main()
