import { Lang } from './i18n';

export function getWhatsAppPitchUrl(lang: Lang): string {
  // Admin can set group links in env
  const en = process.env.NEXT_PUBLIC_WHATSAPP_GROUP_EN || 'https://wa.me/0000000000';
  const fr = process.env.NEXT_PUBLIC_WHATSAPP_GROUP_FR || 'https://wa.me/0000000000';
  return lang === 'fr' ? fr : en;
}
