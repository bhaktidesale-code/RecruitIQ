import axios from "axios";
export const api = axios.create({
  baseURL: 'http://localhost:8000', // Remove the /api/v1
  headers: {
    'Content-Type': 'application/json',
  },
});