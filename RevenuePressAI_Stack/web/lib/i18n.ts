import en from '../locales/en.json';
import fr from '../locales/fr.json';

export type Lang = 'en' | 'fr';

const dict: Record<Lang, Record<string, string>> = {
  en: en as Record<string, string>,
  fr: fr as Record<string, string>,
};

export function getLangFromCookie(cookieHeader?: string | null): Lang {
  const raw = cookieHeader || '';
  const match = raw.match(/(?:^|;\s*)rp_lang=([^;]+)/);
  const val = match?.[1] || 'en';
  return val === 'fr' ? 'fr' : 'en';
}

export function t(lang: Lang, key: string): string {
  return dict[lang][key] || key;
}
