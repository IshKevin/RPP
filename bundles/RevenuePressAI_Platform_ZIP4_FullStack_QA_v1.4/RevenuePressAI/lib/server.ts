import type { GetServerSidePropsContext } from 'next';
import { getLangFromCookie, type Lang } from './i18n';

export function getLang(ctx: GetServerSidePropsContext): Lang {
  const cookie = ctx.req.headers.cookie || null;
  return getLangFromCookie(cookie);
}
