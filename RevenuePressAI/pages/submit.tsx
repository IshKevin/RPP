import type { GetServerSideProps } from 'next';
import { useState } from 'react';
import { Layout } from '../components/Layout';
import { t, type Lang } from '../lib/i18n';
import { getLang } from '../lib/server';

type Props = { lang: Lang };

type FormState = {
  authorName: string;
  authorEmail: string;
  bookTitle: string;
  bookLanguage: 'en' | 'fr' | 'auto';
  description: string;
  amazonLink: string;
};

export default function Submit({ lang }: Props) {
  const tt = t(lang);
  const [loading, setLoading] = useState(false);
  const [msg, setMsg] = useState<string | null>(null);
  const [form, setForm] = useState<FormState>({
    authorName: '',
    authorEmail: '',
    bookTitle: '',
    bookLanguage: 'auto',
    description: '',
    amazonLink: ''
  });

  async function onSubmit(e: React.FormEvent) {
    e.preventDefault();
    setMsg(null);
    setLoading(true);
    try {
      const res = await fetch('/api/books/submit', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ ...form })
      });
      const data = await res.json();
      if (!res.ok) throw new Error(data?.error || 'Request failed');
      setMsg(`${tt('submit_success')} ID: ${data.bookId}`);
      setForm({ authorName: '', authorEmail: '', bookTitle: '', bookLanguage: 'auto', description: '', amazonLink: '' });
    } catch (err: any) {
      setMsg(err.message || 'Error');
    } finally {
      setLoading(false);
    }
  }

  return (
    <Layout lang={lang} title={tt('nav_submit')}>
      <div className="container">
        <div className="card">
          <h1 className="h1">{tt('submit_title')}</h1>
          <p className="muted">{tt('submit_sub')}</p>

          <form onSubmit={onSubmit} className="form">
            <label>
              {tt('field_author_name')}
              <input value={form.authorName} onChange={e => setForm({ ...form, authorName: e.target.value })} required />
            </label>
            <label>
              {tt('field_author_email')}
              <input type="email" value={form.authorEmail} onChange={e => setForm({ ...form, authorEmail: e.target.value })} required />
            </label>
            <label>
              {tt('field_book_title')}
              <input value={form.bookTitle} onChange={e => setForm({ ...form, bookTitle: e.target.value })} required />
            </label>
            <label>
              {tt('field_language')}
              <select value={form.bookLanguage} onChange={e => setForm({ ...form, bookLanguage: e.target.value as any })}>
                <option value="auto">{tt('lang_auto')}</option>
                <option value="en">English</option>
                <option value="fr">Français</option>
              </select>
            </label>
            <label>
              {tt('field_description')}
              <textarea rows={5} value={form.description} onChange={e => setForm({ ...form, description: e.target.value })} required />
            </label>
            <label>
              {tt('field_amazon')}
              <input value={form.amazonLink} onChange={e => setForm({ ...form, amazonLink: e.target.value })} placeholder="https://..." />
            </label>

            <button className="btn" disabled={loading}>
              {loading ? tt('loading') : tt('submit_cta')}
            </button>
            {msg && <p className="muted" style={{ marginTop: 10 }}>{msg}</p>}
          </form>
        </div>
      </div>
    </Layout>
  );
}

export const getServerSideProps: GetServerSideProps<Props> = async (ctx) => {
  return { props: { lang: getLang(ctx) } };
};
