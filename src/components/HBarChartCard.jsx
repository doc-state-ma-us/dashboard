import {
  ResponsiveContainer,
  BarChart,
  Bar,
  XAxis,
  YAxis,
  Tooltip,
  CartesianGrid,
  LabelList,
} from "recharts";

export default function HBarChartCard({ title, data }) {
    const chartHeight = Math.max(420, data.length * 34);
  return (
    <div className="card cardPad">
      <div style={{ display: "flex", justifyContent: "space-between", alignItems: "baseline" }}>
        <h3 className="title">{title}</h3>
        <span className="muted">{data?.length ? `${data.length} groups` : "No data"}</span>
      </div>
      

      <div style={{ height: chartHeight, marginTop: 10 }}>
        <ResponsiveContainer width="100%" height="100%">
          <BarChart
            data={data}
            layout="vertical"
            margin={{ top: 10, right: 30, left: 10, bottom: 10 }}
          >
            <CartesianGrid strokeDasharray="3 3" />
            <XAxis type="number" tick={{ fontSize: 12 }} />
            <YAxis
              type="category"
              dataKey="label"
              width={140}
              tick={{ fontSize: 12 }}
            />
            <Tooltip />
            <Bar dataKey="value" fill="#3b82f6" radius={0}>
              {/* value label at end of bar */}
              <LabelList dataKey="value" position="right" style={{ fontSize: 11, fontWeight: 800 }} />
            </Bar>
          </BarChart>
        </ResponsiveContainer>
      </div>
    </div>
  );
}
