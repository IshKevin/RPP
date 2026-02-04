import { NextRequest, NextResponse } from 'next/server';

const COOKIE = 'rp_lang';
const SUPPORTED = ['en', 'fr'] as const;

type Lang = typeof SUPPORTED[number];

function detectLang(req: NextRequest): Lang {
  const existing = req.cookies.get(COOKIE)?.value;
  if (existing && SUPPORTED.includes(existing as Lang)) return existing as Lang;

  const header = req.headers.get('accept-language') || '';
  const best = header.split(',')[0]?.trim().slice(0,2).toLowerCase();
  if (best === 'fr') return 'fr';
  return 'en';
}

export function middleware(req: NextRequest) {
  const res = NextResponse.next();
  const lang = detectLang(req);
  res.cookies.set(COOKIE, lang, { path: '/', sameSite: 'lax' });
  return res;
}

export const config = {
  matcher: ['/((?!_next/static|_next/image|favicon.ico|robots.txt|sitemap.xml).*)'],
};
