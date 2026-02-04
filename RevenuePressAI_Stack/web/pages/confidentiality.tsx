import type { GetServerSideProps } from 'next';
import { Layout } from '../components/Layout';
import { t, type Lang } from '../lib/i18n';
import { getLang } from '../lib/server';

export default function Confidentiality({ lang }: { lang: Lang }) {
  const tt = t(lang);
  return (
    <Layout lang={lang} title={`${tt('conf_title')} — RevenuePress AI`}>
      <div className="section">
        <h1>{tt('conf_title')}</h1>
        <p className="muted">{tt('conf_sub')}</p>
        <div className="card">
          <h2>Author content control</h2>
          <ul>
            <li>By default, newly submitted books are private (dashboard only).</li>
            <li>Public listing requires an explicit toggle (to be implemented in auth/admin).</li>
          </ul>
          <h2>Operational safeguards</h2>
          <ul>
            <li>Role-based access (admin, author, operator).</li>
            <li>Audit log for exports and pack downloads.</li>
            <li>Configurable NDAs for managed marketing services.</li>
          </ul>
          <p>
            This page is a product placeholder — use your official legal text for production.
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
