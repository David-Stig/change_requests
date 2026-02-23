import axios from 'axios';
import {
  ChangeRequest,
  CreateChangeRequestPayload,
  DashboardSummary,
  Functionality,
  SystemItem,
  User
} from './types';

const api = axios.create({
  baseURL: process.env.NEXT_PUBLIC_API_BASE_URL ?? '/api',
  withCredentials: true
});

export const authApi = {
  login: (username: string, password: string) =>
    api.post('/token/', { username, password }),
  logout: () => api.post('/auth/logout'),
  me: () => api.get<User>('/auth/me')
};

export const dashboardApi = {
  getSummary: () => api.get<DashboardSummary>('/dashboard/summary')
};

export const systemsApi = {
  listSystems: () => api.get<SystemItem[]>('/systems'),
  listFunctionalities: (systemId?: number) =>
    api.get<Functionality[]>('/functionalities', {
      params: systemId ? { systemId } : undefined
    })
};

export const changeRequestsApi = {
  list: () => api.get<ChangeRequest[]>('/change-requests'),
  detail: (id: string) => api.get<ChangeRequest>(`/change-requests/${id}`),
  create: (payload: CreateChangeRequestPayload) =>
    api.post<ChangeRequest>('/change-requests', payload)
};

export default api;
