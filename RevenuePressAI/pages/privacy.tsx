import type { GetServerSideProps } from 'next';
import { Layout } from '../components/Layout';
import { t, type Lang } from '../lib/i18n';
import { getLang } from '../lib/server';

export default function Privacy({ lang }: { lang: Lang }) {
  const tt = t(lang);
  return (
    <Layout lang={lang} title={`${tt('privacy_title')} — RevenuePress AI`}>
      <div className="section">
        <h1>{tt('privacy_title')}</h1>
        <p className="muted">{tt('privacy_sub')}</p>
        <div className="card">
          <h2>1. What we collect</h2>
          <ul>
            <li>Author profile: name, email, optional website & bio.</li>
            <li>Book data: title, language, genre, description, and optional links you provide.</li>
            <li>Usage analytics: basic, privacy‑preserving metrics (page views, clicks, conversions) if enabled.</li>
          </ul>
          <h2>2. What we do not do</h2>
          <ul>
            <li>No sale of personal data.</li>
            <li>No hidden tracking pixels in downloadable assets.</li>
            <li>No unauthorized public listing: authors control visibility.</li>
          </ul>
          <h2>3. Legal & compliance</h2>
          <p>
            GDPR‑ready principles: data minimization, purpose limitation, access & deletion requests, and secure storage.
            This page is a placeholder — replace with a lawyer‑reviewed policy before production.
          </p>
        </div>
      </div>
    </Layout>
  );
}

export const getServerSideProps: GetServerSideProps<{ lang: Lang }> = async (ctx) => {
  const lang = getLang(ctx);
  return { props: { lang } };
};
