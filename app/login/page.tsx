'use client';

import { FormEvent, useState } from 'react';
import { useAuth } from '@/context/AuthContext';

export default function LoginPage() {
  const { login } = useAuth();
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const [error, setError] = useState('');
  const [isSubmitting, setIsSubmitting] = useState(false);

  const handleSubmit = async (event: FormEvent<HTMLFormElement>) => {
    event.preventDefault();
    setError('');
    setIsSubmitting(true);

    try {
      await login(username, password);
    } catch {
      setError('Invalid credentials.');
    } finally {
      setIsSubmitting(false);
    }
  };

  return (
    <div className="flex min-h-screen items-center justify-center p-4">
      <form className="w-full max-w-md space-y-4 rounded-lg bg-white p-6 shadow" onSubmit={handleSubmit}>
        <h1 className="text-2xl font-semibold">Login</h1>
        <div>
          <label htmlFor="username" className="mb-1 block text-sm text-slate-600">
            Username
          </label>
          <input
            id="username"
            className="w-full rounded-md border border-slate-300 px-3 py-2"
            value={username}
            onChange={(event) => setUsername(event.target.value)}
            required
          />
        </div>
        <div>
          <label htmlFor="password" className="mb-1 block text-sm text-slate-600">
            Password
          </label>
          <input
            id="password"
            type="password"
            className="w-full rounded-md border border-slate-300 px-3 py-2"
            value={password}
            onChange={(event) => setPassword(event.target.value)}
            required
          />
        </div>
        {error ? <p className="text-sm text-red-600">{error}</p> : null}
        <button
          type="submit"
          className="w-full rounded-md bg-slate-900 px-3 py-2 text-white disabled:opacity-70"
          disabled={isSubmitting}
        >
          {isSubmitting ? 'Signing in...' : 'Sign in'}
        </button>
      </form>
    </div>
  );
}
