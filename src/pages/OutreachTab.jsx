import { useEffect, useState } from "react";
import DateRange from "../components/DateRange";
import KpiCard from "../components/KpiCard";
import BarChartCard from "../components/BarChartCard";
import PieChartCard from "../components/PieChartCard";
import { fetchOutreachDashboard } from "../api/dashboardApi";
import HBarChartCard from "../components/HBarChartCard";

export default function OutreachTab() {
  const [range, setRange] = useState({ start: "2026-02-21", end: "2026-02-27" });
  const [data, setData] = useState(null);
  const [loading, setLoading] = useState(false);
  const [err, setErr] = useState("");

  async function load(start, end) {
    setLoading(true);
    setErr("");
    try {
      const res = await fetchOutreachDashboard(start, end);
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
      <div><p className="sub">Use this tab to track internal recruitment process and what recruiters are doing as a team during the selected dates. This faster loop of chain of events for candidates helps team to gage the level of interest per quarter.
 </p>
 
        </div>

      <div className="kpiCenter">
        <KpiCard
          title="Total Actions Taken"
          value={data?.kpis?.total_actions_taken ?? (loading ? "…" : 0)}
          accent="var(--green)"
        />
      </div>


      <div className="grid gridFull">
        <HBarChartCard title="Cycle Stage" data={data?.charts?.cycle_stage_bar || []} />
      </div>

      <div className="grid grid2">
        <PieChartCard title="Actions" data={data?.charts?.action_pie || []} />
        <BarChartCard title="Outcome" data={data?.charts?.outcome_bar || []} />
      </div>

      <div className="grid gridFull">
      <HBarChartCard
        title="Recruiter Assessment"
        data={data?.charts?.recruiter_assessment_bar || []}
      />
    </div>
    </div>
  );
}
