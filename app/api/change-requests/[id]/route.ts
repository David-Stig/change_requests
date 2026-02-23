import { cookies } from 'next/headers';
import { NextResponse } from 'next/server';
import serverApi from '@/lib/serverApi';

export async function GET(_: Request, { params }: { params: { id: string } }) {
  try {
    const token = cookies().get('access_token')?.value;
    const response = await serverApi.get(`/api/change-requests/${params.id}/`, {
      headers: { Authorization: `Bearer ${token}` }
    });

    return NextResponse.json(response.data);
  } catch {
    return NextResponse.json({ detail: 'Not found' }, { status: 404 });
  }
}
