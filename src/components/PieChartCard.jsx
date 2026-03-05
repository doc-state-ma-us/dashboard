import { ResponsiveContainer, PieChart, Pie, Tooltip, Legend, Cell } from "recharts";

const COLORS = [
  "#2563eb", "#22c55e", "#f59e0b", "#a855f7", "#ef4444",
  "#06b6d4", "#10b981", "#f97316", "#84cc16", "#8b5cf6",
];

function renderPercentLabel({ cx, cy, midAngle, outerRadius, percent }) {
  // position text a bit outside the slice
  const RADIAN = Math.PI / 180;
  const r = outerRadius + 16;
  const x = cx + r * Math.cos(-midAngle * RADIAN);
  const y = cy + r * Math.sin(-midAngle * RADIAN);

  const p = Math.round((percent || 0) * 100);
  if (p === 0) return null;

  return (
    <text
      x={x}
      y={y}
      fill="#0f172a"
      textAnchor={x > cx ? "start" : "end"}
      dominantBaseline="central"
      fontSize={12}
      fontWeight={800}
    >
      {p}%
    </text>
  );
}

export default function PieChartCard({ title, data }) {
  return (
    <div className="card cardPad">
      <div style={{ display: "flex", justifyContent: "space-between", alignItems: "baseline" }}>
        <h3 className="title">{title}</h3>
        <span className="muted">{data?.length ? `${data.length} slices` : "No data"}</span>
      </div>

      <div style={{ height: 360, marginTop: 10 }}>
        <ResponsiveContainer width="100%" height="100%">
          <PieChart>
            <Pie
              data={data}
              dataKey="value"
              nameKey="label"
              cx="50%"
              cy="45%"
              outerRadius={120}
              stroke="#ffffff"
              strokeWidth={2}
              labelLine={true}
              label={renderPercentLabel}   // ✅ percent labels
            >
              {data?.map((_, i) => (
                <Cell key={i} fill={COLORS[i % COLORS.length]} />
              ))}
            </Pie>

            <Tooltip />
            <Legend
              layout="horizontal"
              verticalAlign="bottom"
              align="center"
              wrapperStyle={{ fontSize: 12 }}
            />
          </PieChart>
        </ResponsiveContainer>
      </div>
    </div>
  );
}
