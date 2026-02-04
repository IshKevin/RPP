import Link from 'next/link';
import type { GetServerSideProps } from 'next';
import { Layout } from '../components/Layout';
import { t, type Lang } from '../lib/i18n';
import { getLang } from '../lib/server';
import { ViralWidgets } from '../components/ViralWidgets';

type Props = { lang: Lang };

export default function Home({ lang }: Props) {
  const tt = t(lang);
  return (
    <Layout lang={lang}>
      <section className="hero">
        <div style={{display:'flex',gap:24,flexWrap:'wrap',alignItems:'center'}}>
          <div style={{flex:'1 1 520px',minWidth:320}}>
            <div style={{fontSize:14,color:'var(--muted)',letterSpacing:0.3,marginBottom:8}}>{tt('tagline')}</div>
            <h1 style={{fontSize:40,lineHeight:1.1,margin:'0 0 12px 0'}}>{tt('hero_title')}</h1>
            <p style={{fontSize:18,color:'var(--muted)',marginTop:0}}>{tt('hero_sub')}</p>
            <div style={{display:'flex',gap:12,flexWrap:'wrap',marginTop:16}}>
              <Link className="btn" href="/submit">{tt('cta_primary')}</Link>
              <Link className="btn secondary" href="/dashboard">{tt('cta_secondary')}</Link>
            </div>
            <div style={{display:'flex',gap:12,flexWrap:'wrap',marginTop:18}}>
              <span className="pill">{tt('pill_1')}</span>
              <span className="pill">{tt('pill_2')}</span>
              <span className="pill">{tt('pill_3')}</span>
            </div>
          </div>
          <div style={{flex:'1 1 360px',minWidth:300}}>
            <div className="card" style={{padding:18}}>
              <div style={{fontWeight:800,fontSize:16,marginBottom:8}}>{tt('in7s_title')}</div>
              <ol style={{margin:0,paddingLeft:18,color:'var(--muted)'}}>
                <li style={{marginBottom:8}}>{tt('in7s_1')}</li>
                <li style={{marginBottom:8}}>{tt('in7s_2')}</li>
                <li>{tt('in7s_3')}</li>
              </ol>
              <div style={{marginTop:14,display:'flex',gap:10,flexWrap:'wrap'}}>
                <span className="pill">{tt('in7s_box_1')}</span>
                <span className="pill">{tt('in7s_box_2')}</span>
                <span className="pill">{tt('in7s_box_3')}</span>
              </div>
              <div style={{marginTop:16,fontSize:13,color:'var(--muted)'}}>
                {tt('disclaimer_small')}
              </div>
            </div>
          </div>
        </div>
      </section>

      <ViralWidgets lang={lang} />

      <section className="section" style={{marginTop:26}}>
        <div className="grid2">
          <div className="card">
            <div className="h2">{tt('what_you_get_title')}</div>
            <ul className="ul">
              <li>{tt('what_you_get_1')}</li>
              <li>{tt('what_you_get_2')}</li>
              <li>{tt('what_you_get_3')}</li>
              <li>{tt('what_you_get_4')}</li>
              <li>{tt('what_you_get_5')}</li>
            </ul>
          </div>
          <div className="card">
            <div className="h2">{tt('who_for_title')}</div>
            <ul className="ul">
              <li>{tt('who_for_1')}</li>
              <li>{tt('who_for_2')}</li>
              <li>{tt('who_for_3')}</li>
              <li>{tt('who_for_4')}</li>
            </ul>
            <div style={{marginTop:14}}>
              <Link className="btn" href="/submit">{tt('cta_primary')}</Link>
            </div>
          </div>
        </div>
      </section>

      <section className="section" style={{marginTop:26}}>
        <div className="card">
          <div className="h2">{tt('video_placeholder_title')}</div>
          <p className="muted">{tt('video_placeholder_copy')}</p>
          <div className="videoPlaceholder">
            <div style={{fontWeight:800}}>{tt('video_placeholder_label')}</div>
            <div className="muted" style={{marginTop:6}}>{tt('video_placeholder_hint')}</div>
          </div>
        </div>
      </section>

      <footer style={{margin:'32px 0 10px 0',color:'var(--muted)',fontSize:13}}>
        <div>{tt('footer_privacy')} · <Link href="/privacy">{tt('privacy_policy')}</Link> · <Link href="/confidentiality">{tt('confidentiality')}</Link></div>
      </footer>
    </Layout>
  );
}

export const getServerSideProps: GetServerSideProps<Props> = async (ctx) => {
  return { props: { lang: getLang(ctx) } };
};
