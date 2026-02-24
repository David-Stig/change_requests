import axios from 'axios';

const serverApi = axios.create({
  baseURL: process.env.BACKEND_API_URL,
  withCredentials: true
});

export default serverApi;
