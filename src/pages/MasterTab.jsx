import { useEffect, useState } from "react";
import DateRange from "../components/DateRange";
import KpiCard from "../components/KpiCard";
import BarChartCard from "../components/BarChartCard";
import PieChartCard from "../components/PieChartCard";
import { fetchMasterDashboard } from "../api/dashboardApi";

export default function MasterTab() {
  const [range, setRange] = useState({ start: "2026-02-21", end: "2026-02-27" });
  const [data, setData] = useState(null);
  const [loading, setLoading] = useState(false);
  const [err, setErr] = useState("");

  async function load(start, end) {
    setLoading(true);
    setErr("");
    try {
      const res = await fetchMasterDashboard(start, end);
      setData(res);
      setRange({ start, end });
    } catch (e) {
      setErr(e?.response?.data?.detail || e.message || "Error");
      setData(null);
    } finally {
      setLoading(false);
    }
  }

  // initial load once
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
      <div><p className="sub">Use this tab to track new candidates added during the selected dates, where they came from, and which recruiters are handling them.</p>
        </div>
      <div className="kpiCenter">
        <KpiCard
          title="New Candidates"
          value={data?.kpis?.new_candidates ?? (loading ? "…" : 0)}
          accent="var(--blue)"
        />
</div>

      <div className="grid grid2">
        <BarChartCard title="Source (New Candidates)" data={data?.charts?.source_bar || []} />
        <PieChartCard title="Recruiter Assigned (New Candidates)" data={data?.charts?.recruiter_donut || []} />
      </div>
    </div>
  );
}
