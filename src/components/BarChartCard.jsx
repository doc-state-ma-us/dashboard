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

// --- CUSTOM TICK COMPONENT ---
const CustomXAxisTick = ({ x, y, payload }) => {
  // Split by space, but also by forward slashes if they exist
  const words = payload.value.split(/[\s/]+/); 
  
  return (
    <g transform={`translate(${x},${y})`}>
      <text
        x={0}
        y={0}
        dy={25} // 1. Increased this to move the whole block away from the line
        textAnchor="middle"
        fill="#666"
        style={{ fontSize: 12, lineHeight: '1.2' }}
      >
        {words.map((word, index) => (
          <tspan 
            x={0} // 2. Ensures every word stays centered under the bar
            dy={index === 0.1 ? "0em" : "1.1em"} 
            key={index}
          >
            {word}
          </tspan>
        ))}
      </text>
    </g>
  );
};

export default function BarChartCard({ title, data }) {
  return (
    <div className="card cardPad">
      <div style={{ display: "flex", justifyContent: "space-between", alignItems: "baseline" }}>
        <h3 className="title">{title}</h3>
        <span className="muted">{data?.length ? `${data.length} groups` : "No data"}</span>
      </div>

      <div style={{ height: 380, marginTop: 10 }}> {/* Increased height slightly for wrapped text */}
        <ResponsiveContainer width="100%" height="100%">
          <BarChart data={data} margin={{ top: 25, right: 10, left: 0, bottom: 90 }}> {/* Increased bottom margin */}
            <CartesianGrid strokeDasharray="3 3" />
            <XAxis
              dataKey="label"
              interval={0}
              height={10} // Give the text more room to grow vertically
              tick={<CustomXAxisTick />} 
              axisLine={{ stroke: '#E6E6E6' }}
            />
            <YAxis tick={{ fontSize: 12 }} />
            <Tooltip />
            <Bar dataKey="value" fill="#085ea3">
              <LabelList dataKey="value" position="top" style={{ fontSize: 12, fontWeight: 800 }} />
            </Bar>
          </BarChart>
        </ResponsiveContainer>
      </div>
    </div>
  );
}