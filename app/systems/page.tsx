'use client';

import { useEffect, useState } from 'react';
import { ProtectedLayout } from '@/components/auth/ProtectedLayout';
import { systemsApi } from '@/lib/api';
import { SystemItem } from '@/lib/types';

export default function SystemsPage() {
  const [systems, setSystems] = useState<SystemItem[]>([]);

  useEffect(() => {
    const fetchSystems = async () => {
      const response = await systemsApi.listSystems();
      setSystems(response.data);
    };

    void fetchSystems();
  }, []);

  return (
    <ProtectedLayout>
      <section className="rounded-lg border border-slate-200 bg-white p-4">
        <h2 className="mb-4 text-2xl font-semibold">Systems</h2>
        <ul className="space-y-2">
          {systems.map((system) => (
            <li key={system.id} className="rounded-md border border-slate-200 px-3 py-2">
              {system.name}
            </li>
          ))}
        </ul>
      </section>
    </ProtectedLayout>
  );
}
