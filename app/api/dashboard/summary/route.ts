import { cookies } from 'next/headers';
import { NextResponse } from 'next/server';
import serverApi from '@/lib/serverApi';

export async function GET() {
  try {
    const token = cookies().get('access_token')?.value;
    const response = await serverApi.get('/api/dashboard/summary/', {
      headers: { Authorization: `Bearer ${token}` }
    });

    return NextResponse.json(response.data);
  } catch {
    return NextResponse.json({ totalCrCount: 0, mySubmittedCrs: 0, pendingApprovals: 0 });
  }
}
