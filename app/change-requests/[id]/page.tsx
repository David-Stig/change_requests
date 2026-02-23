'use client';

import { useEffect, useState } from 'react';
import { ProtectedLayout } from '@/components/auth/ProtectedLayout';
import { changeRequestsApi } from '@/lib/api';
import { ChangeRequest } from '@/lib/types';

export default function ChangeRequestDetailPage({ params }: { params: { id: string } }) {
  const [request, setRequest] = useState<ChangeRequest | null>(null);

  useEffect(() => {
    const fetchRequest = async () => {
      const response = await changeRequestsApi.detail(params.id);
      setRequest(response.data);
    };

    void fetchRequest();
  }, [params.id]);

  return (
    <ProtectedLayout>
      <section className="rounded-lg border border-slate-200 bg-white p-4">
        <h2 className="text-2xl font-semibold">Change Request Detail</h2>
        {request ? (
          <div className="mt-4 space-y-2 text-sm">
            <p>
              <strong>Title:</strong> {request.title}
            </p>
            <p>
              <strong>Description:</strong> {request.description}
            </p>
            <p>
              <strong>System:</strong> {request.system.name}
            </p>
            <p>
              <strong>Functionality:</strong> {request.functionality.name}
            </p>
            <p>
              <strong>Category:</strong> {request.changeCategory}
            </p>
            <p>
              <strong>Status:</strong> {request.status}
            </p>
          </div>
        ) : null}
      </section>
    </ProtectedLayout>
  );
}
