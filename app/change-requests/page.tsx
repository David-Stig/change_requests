'use client';

import Link from 'next/link';
import { useEffect, useState } from 'react';
import { ProtectedLayout } from '@/components/auth/ProtectedLayout';
import { changeRequestsApi } from '@/lib/api';
import { ChangeRequest } from '@/lib/types';

export default function ChangeRequestsPage() {
  const [requests, setRequests] = useState<ChangeRequest[]>([]);

  useEffect(() => {
    const fetchRequests = async () => {
      const response = await changeRequestsApi.list();
      setRequests(response.data);
    };

    void fetchRequests();
  }, []);

  return (
    <ProtectedLayout>
      <section className="rounded-lg border border-slate-200 bg-white p-4">
        <h2 className="mb-4 text-2xl font-semibold">Change Requests</h2>
        <div className="space-y-3">
          {requests.map((request) => (
            <Link
              key={request.id}
              href={`/change-requests/${request.id}`}
              className="block rounded-md border border-slate-200 p-3 hover:bg-slate-50"
            >
              <h3 className="font-medium">{request.title}</h3>
              <p className="text-sm text-slate-500">{request.status}</p>
            </Link>
          ))}
        </div>
      </section>
    </ProtectedLayout>
  );
}
