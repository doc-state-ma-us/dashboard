import { useEffect, useState } from "react";
import DateRange from "../components/DateRange";
import BarChartCard from "../components/BarChartCard";
import PieChartCard from "../components/PieChartCard";
import KpiCard from "../components/KpiCard";
import { fetchExamDashboard } from "../api/dashboardApi";

export default function ExamTab() {
  const [range, setRange] = useState({ start: "2026-02-21", end: "2026-02-27" });
  const [data, setData] = useState(null);
  const [loading, setLoading] = useState(false);
  const [err, setErr] = useState("");

  async function load(start, end) {
    setLoading(true);
    setErr("");
    try {
      const res = await fetchExamDashboard(start, end);
      setData(res);
      setRange({ start, end });
    } catch (e) {
      setErr(e?.response?.data?.detail || e.message || "Error");
      setData(null);
    } finally {
      setLoading(false);
    }
  }

  useEffect(() => {
    load(range.start, range.end);
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, []);

  return (
    <div className="grid" style={{ marginTop: 14 }}>
      <DateRange
        initialStart={range.start}
        initialEnd={range.end}
        onApply={(s, e) => load(s, e)}
      />

      {err && <div className="error">{err}</div>}
      <div><p className="sub">Use this tab to track what recruiters are doing as a team during the selected dates with the candidates who are registered or likely to be register for Civil Service Exam.</p>
        </div>

      <div className="kpiRow">
      </div>
      <div className="grid gridFull">
        {/* Full width */}
        <BarChartCard
          title="Exam Cycle Stage"
          data={data?.charts?.exam_cycle_stage_bar || []}
        />
      </div>

      <div className="grid grid2">
        <PieChartCard title="Actions" data={data?.charts?.action_pie || []} />
        <BarChartCard title="Outcome" data={data?.charts?.outcome_bar || []} />
        <BarChartCard title="Recruiter Assessment" data={data?.charts?.recruiter_assessment_bar || []} />
        <PieChartCard title="Recruiter Contribution" data={data?.charts?.recruiter_donut || []} />
      </div>
    </div>
  );
}
