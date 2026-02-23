'use client';

import { useEffect, useState } from 'react';
import { ProtectedLayout } from '@/components/auth/ProtectedLayout';
import { Card } from '@/components/ui/Card';
import { dashboardApi } from '@/lib/api';
import { DashboardSummary } from '@/lib/types';

export default function DashboardPage() {
  const [summary, setSummary] = useState<DashboardSummary | null>(null);

  useEffect(() => {
    const fetchSummary = async () => {
      try {
        const response = await dashboardApi.getSummary();
        setSummary(response.data);
      } catch {
        setSummary({ totalCrCount: 0, mySubmittedCrs: 0, pendingApprovals: 0 });
      }
    };

    void fetchSummary();
  }, []);

  return (
    <ProtectedLayout>
      <section>
        <h2 className="mb-4 text-2xl font-semibold">Dashboard</h2>
        <div className="grid grid-cols-1 gap-4 md:grid-cols-3">
          <Card title="Total CR count" value={summary?.totalCrCount ?? '-'} />
          <Card title="My submitted CRs" value={summary?.mySubmittedCrs ?? '-'} />
          <Card title="Pending approvals" value={summary?.pendingApprovals ?? '-'} />
        </div>
      </section>
    </ProtectedLayout>
  );
}
