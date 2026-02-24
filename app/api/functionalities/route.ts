import { cookies } from 'next/headers';
import { NextRequest, NextResponse } from 'next/server';
import serverApi from '@/lib/serverApi';

export async function GET(request: NextRequest) {
  try {
    const token = cookies().get('access_token')?.value;
    const systemId = request.nextUrl.searchParams.get('systemId');
    const response = await serverApi.get('/api/functionalities/', {
      headers: { Authorization: `Bearer ${token}` },
      params: systemId ? { systemId } : undefined
    });

    return NextResponse.json(response.data);
  } catch {
    return NextResponse.json([]);
  }
}
