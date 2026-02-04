import Head from 'next/head';
import Link from 'next/link';
import { ReactNode, useMemo } from 'react';
import { t, type Lang } from '../lib/i18n';

type Props = {
  lang: Lang;
  title?: string;
  children: ReactNode;
};

export function Layout({ lang, title, children }: Props) {
  const tt = useMemo(() => t(lang), [lang]);
  return (
    <div>
      <Head>
        <title>{title ? `${title} — RevenuePress AI` : 'RevenuePress AI'}</title>
        <meta name="viewport" content="width=device-width, initial-scale=1" />
        <meta name="description" content={tt('meta_desc')} />
      </Head>

      <header className="header">
        <div className="container" style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', gap: 16 }}>
          <div style={{ display: 'flex', alignItems: 'center', gap: 12 }}>
            <div className="logo" aria-label="RevenuePress AI">RP</div>
            <div>
              <div style={{ fontWeight: 800, letterSpacing: 0.2 }}>{tt('brand')}</div>
              <div style={{ fontSize: 12, color: 'var(--muted)' }}>{tt('tagline')}</div>
            </div>
          </div>

          <nav className="nav">
            <Link href="/">{tt('nav_home')}</Link>
            <Link href="/submit">{tt('nav_submit')}</Link>
            <Link href="/dashboard">{tt('nav_dashboard')}</Link>
            <Link href="/pricing">{tt('nav_pricing')}</Link>
            <a className="btn" href={lang === 'fr' ? process.env.NEXT_PUBLIC_WHATSAPP_GROUP_FR || '#' : process.env.NEXT_PUBLIC_WHATSAPP_GROUP_EN || '#'}>
              {tt('nav_whatsapp')}
            </a>
          </nav>
        </div>
      </header>

      <main className="container">{children}</main>

      <footer className="container" style={{ paddingTop: 40, paddingBottom: 60, color: 'var(--muted)' }}>
        <div style={{ display: 'flex', gap: 16, flexWrap: 'wrap', justifyContent: 'space-between' }}>
          <div>© {new Date().getFullYear()} RevenuePress AI</div>
          <div style={{ display: 'flex', gap: 16, flexWrap: 'wrap' }}>
            <Link href="/privacy">{tt('privacy')}</Link>
            <Link href="/confidentiality">{tt('confidentiality')}</Link>
          </div>
        </div>
      </footer>
    </div>
  );
}
