export default function KpiCard({ title, value, accent = "var(--blue)", hint }) {
  return (
    <div className="card cardPad kpiCard">
      <div className="kpiTitle">{title}</div>
      <div className="kpiValueCenter">{value}</div>
      {hint && <div className="kpiHint">{hint}</div>}
      <div className="kpiAccent" style={{ background: accent }} />
    </div>
  );
}