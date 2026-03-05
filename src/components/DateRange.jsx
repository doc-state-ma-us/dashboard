import { useState } from "react";

export default function DateRange({ initialStart, initialEnd, onApply }) {
  const [startDate, setStartDate] = useState(initialStart);
  const [endDate, setEndDate] = useState(initialEnd);

  return (
    <div className="card">
      <div className="toolbar">
        <div className="dateGroup">
          <div className="dateField">
            <label>Start date</label>
            <input type="date" value={startDate} onChange={(e) => setStartDate(e.target.value)} />
          </div>
          <div className="dateField">
            <label>End date</label>
            <input type="date" value={endDate} onChange={(e) => setEndDate(e.target.value)} />
          </div>
        </div>

        <button className="btn btnPrimary" onClick={() => onApply(startDate, endDate)}>
          Apply
        </button>
      </div>
    </div>
  );
}
