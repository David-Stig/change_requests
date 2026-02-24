export type User = {
  id: number;
  username: string;
  email?: string;
  isApprover?: boolean;
};

export type DashboardSummary = {
  totalCrCount: number;
  mySubmittedCrs: number;
  pendingApprovals: number;
};

export type SystemItem = {
  id: number;
  name: string;
};

export type Functionality = {
  id: number;
  name: string;
  systemId: number;
};

export type ChangeRequest = {
  id: number;
  title: string;
  description: string;
  system: SystemItem;
  functionality: Functionality;
  changeCategory: string;
  status: string;
  submittedBy: string;
  createdAt: string;
};

export type CreateChangeRequestPayload = {
  title: string;
  description: string;
  systemId: number;
  functionalityId: number;
  changeCategory: string;
};
