import { useState } from "react";
import MasterTab from "./pages/MasterTab";
import OutreachTab from "./pages/OutreachTab";
import ExamTab from "./pages/ExamTab";

export default function App() {
  const [tab, setTab] = useState("master");

  return (
    <div className="container">
      <div className="header">
        <div>
          <h1 className="h1">DOC Recruitment Dashboard</h1>
          <p className="sub">Select a date range to view counts and distributions.</p>
        </div>

        <div className="tabs">
          <button
            className={`tabBtn ${tab === "master" ? "tabBtnActive" : ""}`}
            onClick={() => setTab("master")}
          >
            Master
          </button>
          <button
            className={`tabBtn ${tab === "outreach" ? "tabBtnActive" : ""}`}
            onClick={() => setTab("outreach")}
          >
            Daily Outreach
          </button>
          <button
            className={`tabBtn ${tab === "exam" ? "tabBtnActive" : ""}`}
            onClick={() => setTab("exam")}
          >
            Exam Tracker
          </button>
        </div>
      </div>

      {tab === "master" && <MasterTab />}
      {tab === "outreach" && <OutreachTab />}
      {tab === "exam" && <ExamTab />}
    </div>
  );
}
