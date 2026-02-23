import { cookies } from 'next/headers';
import { NextRequest, NextResponse } from 'next/server';
import serverApi from '@/lib/serverApi';

export async function GET() {
  try {
    const token = cookies().get('access_token')?.value;
    const response = await serverApi.get('/api/change-requests/', {
      headers: { Authorization: `Bearer ${token}` }
    });

    return NextResponse.json(response.data);
  } catch {
    return NextResponse.json([]);
  }
}

export async function POST(request: NextRequest) {
  try {
    const token = cookies().get('access_token')?.value;
    const payload = await request.json();
    const response = await serverApi.post('/api/change-requests/', payload, {
      headers: { Authorization: `Bearer ${token}` }
    });

    return NextResponse.json(response.data, { status: 201 });
  } catch {
    return NextResponse.json({ detail: 'Unable to create change request' }, { status: 400 });
  }
}
