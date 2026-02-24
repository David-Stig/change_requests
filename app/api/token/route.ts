import { cookies } from 'next/headers';
import { NextRequest, NextResponse } from 'next/server';
import serverApi from '@/lib/serverApi';

const ACCESS_TOKEN_COOKIE = 'access_token';
const REFRESH_TOKEN_COOKIE = 'refresh_token';

export async function POST(request: NextRequest) {
  try {
    const credentials = await request.json();
    const response = await serverApi.post('/api/token/', credentials);
    const { access, refresh } = response.data;

    cookies().set(ACCESS_TOKEN_COOKIE, access, {
      httpOnly: true,
      sameSite: 'lax',
      secure: process.env.NODE_ENV === 'production',
      path: '/',
      maxAge: 60 * 15
    });

    cookies().set(REFRESH_TOKEN_COOKIE, refresh, {
      httpOnly: true,
      sameSite: 'lax',
      secure: process.env.NODE_ENV === 'production',
      path: '/',
      maxAge: 60 * 60 * 24 * 14
    });

    return NextResponse.json({ success: true });
  } catch {
    return NextResponse.json({ detail: 'Invalid credentials' }, { status: 401 });
  }
}
