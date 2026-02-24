import { cookies } from 'next/headers';
import { NextResponse } from 'next/server';
import serverApi from '@/lib/serverApi';

export async function GET() {
  try {
    const token = cookies().get('access_token')?.value;

    if (!token) {
      return NextResponse.json({ detail: 'Unauthorized' }, { status: 401 });
    }

    const response = await serverApi.get('/api/auth/me/', {
      headers: {
        Authorization: `Bearer ${token}`
      }
    });

    return NextResponse.json(response.data);
  } catch {
    return NextResponse.json({ detail: 'Unauthorized' }, { status: 401 });
  }
}
