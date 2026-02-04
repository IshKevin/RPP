import type { GetServerSideProps } from 'next';
import Link from 'next/link';
import { useEffect, useState } from 'react';
import { Layout } from '../components/Layout';
import { t, type Lang } from '../lib/i18n';
import { getLang } from '../lib/server';

type Props = { lang: Lang };

type Book = {
  id: string;
  title: string;
  language: string;
  createdAt: string;
  authorName: string;
};

export default function Dashboard({ lang }: Props) {
  const tt = t(lang);
  const [books, setBooks] = useState<Book[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    (async () => {
      try {
        const res = await fetch('/api/books/list');
        const json = await res.json();
        setBooks(json.books || []);
      } catch (e) {
        setError((e as Error).message);
      } finally {
        setLoading(false);
      }
    })();
  }, []);

  return (
    <Layout lang={lang} title={tt('nav_dashboard')}>
      <div className="section">
        <h1 className="h1">{tt('nav_dashboard')}</h1>
        <p className="muted">{tt('dashboard_intro')}</p>

        {loading && <div className="card">Loading…</div>}
        {error && <div className="card">Error: {error}</div>}

        {!loading && !error && (
          <div className="grid2">
            {books.map((b) => (
              <div key={b.id} className="card">
                <div className="h2">{b.title}</div>
                <p className="muted">
                  {b.authorName} • {b.language.toUpperCase()} • {new Date(b.createdAt).toLocaleDateString()}
                </p>
                <div className="row" style={{ marginTop: 10 }}>
                  <Link className="btn" href={`/books/${b.id}`}>View</Link>
                  <a className="btn outline" href={`/api/assets/placeholder?bookId=${b.id}`}>
                    {tt('download_assets')}
                  </a>
                </div>
              </div>
            ))}
          </div>
        )}
      </div>
    </Layout>
  );
}

export const getServerSideProps: GetServerSideProps<Props> = async (ctx) => {
  return { props: { lang: getLang(ctx) } };
};
