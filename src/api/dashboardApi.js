import axios from "axios";
import { API_BASE_URL } from "../config";

const api = axios.create({
  baseURL: API_BASE_URL,
});

export async function fetchMasterDashboard(startDate, endDate) {
  const res = await api.get("/dashboard/master", {
    params: { start_date: startDate, end_date: endDate },
  });
  return res.data;
}

export async function fetchOutreachDashboard(startDate, endDate) {
  const res = await api.get("/dashboard/outreach", {
    params: { start_date: startDate, end_date: endDate },
  });
  return res.data;
}

export async function fetchExamDashboard(startDate, endDate) {
  const res = await api.get("/dashboard/exam", {
    params: { start_date: startDate, end_date: endDate },
  });
  return res.data;
}
