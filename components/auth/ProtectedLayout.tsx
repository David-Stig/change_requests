'use client';

import Link from 'next/link';
import { useAuth } from '@/context/AuthContext';

export function ProtectedLayout({ children }: { children: React.ReactNode }) {
  const { isAuthenticated, isLoading, logout, user } = useAuth();

  if (isLoading) {
    return (
      <div className="flex min-h-screen items-center justify-center">
        <p className="text-slate-600">Loading...</p>
      </div>
    );
  }

  if (!isAuthenticated) {
    return null;
  }

  return (
    <div className="min-h-screen">
      <header className="border-b border-slate-200 bg-white">
        <div className="mx-auto flex max-w-6xl items-center justify-between px-4 py-4">
          <h1 className="text-xl font-semibold">Change Requests</h1>
          <div className="flex items-center gap-4">
            <span className="text-sm text-slate-600">{user?.username}</span>
            <button
              type="button"
              className="rounded-md bg-slate-900 px-3 py-2 text-sm text-white"
              onClick={() => void logout()}
            >
              Logout
            </button>
          </div>
        </div>
      </header>
      <div className="mx-auto grid max-w-6xl grid-cols-1 gap-4 px-4 py-6 md:grid-cols-[220px_1fr]">
        <aside className="rounded-lg border border-slate-200 bg-white p-3">
          <nav className="flex flex-col gap-2 text-sm">
            <Link href="/dashboard">Dashboard</Link>
            <Link href="/systems">Systems</Link>
            <Link href="/change-requests">Change Requests</Link>
            <Link href="/create-change-request">Create Change Request</Link>
          </nav>
        </aside>
        <main>{children}</main>
      </div>
    </div>
  );
}
