import axios from "axios";

export const loginBackend = axios.create({
  baseURL: "http://localhost:8002",
});
