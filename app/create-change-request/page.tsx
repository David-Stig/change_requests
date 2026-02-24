'use client';

import { FormEvent, useEffect, useMemo, useState } from 'react';
import { useRouter } from 'next/navigation';
import { ProtectedLayout } from '@/components/auth/ProtectedLayout';
import { changeRequestsApi, systemsApi } from '@/lib/api';
import { Functionality, SystemItem } from '@/lib/types';

const CHANGE_CATEGORIES = ['Standard', 'Emergency', 'Routine'];

export default function CreateChangeRequestPage() {
  const [title, setTitle] = useState('');
  const [description, setDescription] = useState('');
  const [systems, setSystems] = useState<SystemItem[]>([]);
  const [functionalities, setFunctionalities] = useState<Functionality[]>([]);
  const [systemId, setSystemId] = useState<number | ''>('');
  const [functionalityId, setFunctionalityId] = useState<number | ''>('');
  const [changeCategory, setChangeCategory] = useState(CHANGE_CATEGORIES[0]);
  const router = useRouter();

  useEffect(() => {
    const fetchData = async () => {
      const systemsResponse = await systemsApi.listSystems();
      setSystems(systemsResponse.data);
      const functionalitiesResponse = await systemsApi.listFunctionalities();
      setFunctionalities(functionalitiesResponse.data);
    };

    void fetchData();
  }, []);

  const filteredFunctionalities = useMemo(() => {
    if (!systemId) {
      return functionalities;
    }

    return functionalities.filter((item) => item.systemId === systemId);
  }, [functionalities, systemId]);

  const handleSubmit = async (event: FormEvent<HTMLFormElement>) => {
    event.preventDefault();

    if (!systemId || !functionalityId) {
      return;
    }

    await changeRequestsApi.create({
      title,
      description,
      systemId,
      functionalityId,
      changeCategory
    });

    router.push('/change-requests');
  };

  return (
    <ProtectedLayout>
      <section className="rounded-lg border border-slate-200 bg-white p-4">
        <h2 className="mb-4 text-2xl font-semibold">Create Change Request</h2>
        <form className="space-y-4" onSubmit={handleSubmit}>
          <div>
            <label htmlFor="title" className="mb-1 block text-sm text-slate-600">
              Title
            </label>
            <input
              id="title"
              className="w-full rounded-md border border-slate-300 px-3 py-2"
              value={title}
              onChange={(event) => setTitle(event.target.value)}
              required
            />
          </div>
          <div>
            <label htmlFor="description" className="mb-1 block text-sm text-slate-600">
              Description
            </label>
            <textarea
              id="description"
              className="min-h-28 w-full rounded-md border border-slate-300 px-3 py-2"
              value={description}
              onChange={(event) => setDescription(event.target.value)}
              required
            />
          </div>
          <div>
            <label htmlFor="system" className="mb-1 block text-sm text-slate-600">
              System
            </label>
            <select
              id="system"
              className="w-full rounded-md border border-slate-300 px-3 py-2"
              value={systemId}
              onChange={(event) => {
                setSystemId(Number(event.target.value));
                setFunctionalityId('');
              }}
              required
            >
              <option value="">Select a system</option>
              {systems.map((system) => (
                <option key={system.id} value={system.id}>
                  {system.name}
                </option>
              ))}
            </select>
          </div>
          <div>
            <label htmlFor="functionality" className="mb-1 block text-sm text-slate-600">
              Functionality
            </label>
            <select
              id="functionality"
              className="w-full rounded-md border border-slate-300 px-3 py-2"
              value={functionalityId}
              onChange={(event) => setFunctionalityId(Number(event.target.value))}
              required
            >
              <option value="">Select a functionality</option>
              {filteredFunctionalities.map((functionality) => (
                <option key={functionality.id} value={functionality.id}>
                  {functionality.name}
                </option>
              ))}
            </select>
          </div>
          <div>
            <label htmlFor="changeCategory" className="mb-1 block text-sm text-slate-600">
              Change Category
            </label>
            <select
              id="changeCategory"
              className="w-full rounded-md border border-slate-300 px-3 py-2"
              value={changeCategory}
              onChange={(event) => setChangeCategory(event.target.value)}
            >
              {CHANGE_CATEGORIES.map((category) => (
                <option key={category} value={category}>
                  {category}
                </option>
              ))}
            </select>
          </div>
          <button type="submit" className="rounded-md bg-slate-900 px-4 py-2 text-white">
            Submit
          </button>
        </form>
      </section>
    </ProtectedLayout>
  );
}
