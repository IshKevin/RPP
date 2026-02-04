import type { GetServerSideProps } from 'next';
import { useEffect, useState } from 'react';
import Link from 'next/link';
import { Layout } from '../../components/Layout';
import { t, type Lang } from '../../lib/i18n';
import { getLang } from '../../lib/server';

type Props = { lang: Lang; id: string };

type LaunchPack = {
  targetAudiences?: string[];
  bestChannels?: { channel: string; why: string; cta: string; message: string }[];
  emotionalReach?: string[];
  gifts?: string[];
  keywords?: string[];
  hashtags?: string[];
  adScripts?: { angle: string; script: string; footageIdeas: string[] }[];
  visualsBrief?: string[];
  pricing?: { tier: string; includes: string[]; priceMonthlyUSD: number }[];
  paymentMethods?: string[];
};

type BookResponse = {
  ok: boolean;
  book?: {
    id: string;
    title: string;
    language: string;
    description: string | null;
    genre: string | null;
    authorName: string;
    createdAt: string;
    pack: LaunchPack | null;
  };
  error?: string;
};

export default function BookDetail({ lang, id }: Props) {
  const tt = t(lang);
  const [data, setData] = useState<BookResponse | null>(null);
  const [err, setErr] = useState<string | null>(null);

  useEffect(() => {
    (async () => {
      try {
        const r = await fetch(`/api/books/get?id=${encodeURIComponent(id)}`);
        const j: BookResponse = await r.json();
        setData(j);
        if (!j.ok) setErr(j.error || 'Error');
      } catch (e: any) {
        setErr(e?.message || 'Error');
      }
    })();
  }, [id]);

  const book = data?.book;
  const pack = book?.pack || {};

  return (
    <Layout lang={lang} title={book ? `${book.title} — RevenuePress AI` : 'RevenuePress AI'}>
      <div className="section">
        <Link href="/dashboard">← {tt('nav_dashboard')}</Link>
        <h1 style={{ marginTop: 10 }}>{book?.title || '...'}</h1>
        <p className="muted">
          {book ? `${book.authorName} • ${new Date(book.createdAt).toLocaleDateString()} • ${book.language.toUpperCase()}` : ''}
        </p>
        {book?.description ? <p>{book.description}</p> : null}
        {err ? <p style={{ color: 'crimson' }}>{err}</p> : null}
      </div>

      <div className="grid2">
        <div className="card">
          <div className="h2">{tt('pack_title')}</div>
          <p className="muted">{tt('pack_sub')}</p>
          <ul>
            {(pack.targetAudiences || []).map((x, i) => (
              <li key={i}>{x}</li>
            ))}
          </ul>
        </div>

        <div className="card">
          <div className="h2">{tt('pack_keywords')}</div>
          <p className="muted">{tt('pack_keywords_sub')}</p>
          <div style={{ display: 'flex', flexWrap: 'wrap', gap: 8 }}>
            {(pack.keywords || []).map((k, i) => (
              <span key={i} className="pill">{k}</span>
            ))}
          </div>
          <div style={{ height: 12 }} />
          <div style={{ display: 'flex', flexWrap: 'wrap', gap: 8 }}>
            {(pack.hashtags || []).map((h, i) => (
              <span key={i} className="pill">{h}</span>
            ))}
          </div>
        </div>

        <div className="card">
          <div className="h2">{tt('pack_channels')}</div>
          <p className="muted">{tt('pack_channels_sub')}</p>
          {(pack.bestChannels || []).map((c, i) => (
            <div key={i} style={{ padding: '10px 0', borderTop: i ? '1px solid var(--grey)' : 'none' }}>
              <b>{c.channel}</b>
              <div className="muted" style={{ marginTop: 4 }}>{c.why}</div>
              <div style={{ marginTop: 8 }}><b>{tt('pack_message')}:</b> {c.message}</div>
              <div style={{ marginTop: 4 }}><b>{tt('pack_cta')}:</b> {c.cta}</div>
            </div>
          ))}
        </div>

        <div className="card">
          <div className="h2">{tt('pack_ads')}</div>
          <p className="muted">{tt('pack_ads_sub')}</p>
          {(pack.adScripts || []).map((a, i) => (
            <div key={i} style={{ padding: '10px 0', borderTop: i ? '1px solid var(--grey)' : 'none' }}>
              <b>{a.angle}</b>
              <p style={{ whiteSpace: 'pre-wrap' }}>{a.script}</p>
              <div className="muted"><b>{tt('pack_footage')}:</b> {a.footageIdeas?.join(' • ')}</div>
            </div>
          ))}
        </div>

        <div className="card">
          <div className="h2">{tt('pack_emotion')}</div>
          <p className="muted">{tt('pack_emotion_sub')}</p>
          <ul>
            {(pack.emotionalReach || []).map((x, i) => (
              <li key={i}>{x}</li>
            ))}
          </ul>
          <div className="h2" style={{ marginTop: 14 }}>{tt('pack_gift')}</div>
          <p className="muted">{tt('pack_gift_sub')}</p>
          <ul>
            {(pack.gifts || []).map((x, i) => (
              <li key={i}>{x}</li>
            ))}
          </ul>
        </div>

        <div className="card">
          <div className="h2">{tt('pack_payments')}</div>
          <p className="muted">{tt('pack_payments_sub')}</p>
          <div style={{ display: 'flex', flexWrap: 'wrap', gap: 8 }}>
            {(pack.paymentMethods || []).map((p, i) => (
              <span key={i} className="pill">{p}</span>
            ))}
          </div>
          <div className="h2" style={{ marginTop: 14 }}>{tt('pack_pricing')}</div>
          <p className="muted">{tt('pack_pricing_sub')}</p>
          {(pack.pricing || []).map((tier, i) => (
            <div key={i} style={{ padding: '10px 0', borderTop: i ? '1px solid var(--grey)' : 'none' }}>
              <b>{tier.tier}</b> — ${tier.priceMonthlyUSD}/mo
              <ul>
                {tier.includes.map((x, j) => (
                  <li key={j}>{x}</li>
                ))}
              </ul>
            </div>
          ))}
        </div>
      </div>
    </Layout>
  );
}

export const getServerSideProps: GetServerSideProps<Props> = async (ctx) => {
  const lang = getLang(ctx);
  const id = String(ctx.params?.id || '');
  return { props: { lang, id } };
};
