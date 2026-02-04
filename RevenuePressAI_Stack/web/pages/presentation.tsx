import type { GetServerSideProps } from 'next';
import { Layout } from '../components/Layout';
import { t, type Lang } from '../lib/i18n';
import { getLang } from '../lib/server';

export default function Presentation({ lang }: { lang: Lang }) {
  const tt = t(lang);
  return (
    <Layout lang={lang} title={`${tt('presentation_title')} — RevenuePress AI`}>
      <div className="section">
        <h1>{tt('presentation_title')}</h1>
        <p className="muted">{tt('presentation_sub')}</p>
        <div className="card">
          <div style={{aspectRatio:'16/9',background:'#000',borderRadius:16,display:'flex',alignItems:'center',justifyContent:'center'}}>
            <div style={{color:'#fff',textAlign:'center',padding:24}}>
              <div style={{fontSize:18,fontWeight:700}}>{tt('presentation_placeholder')}</div>
              <div style={{opacity:0.8,marginTop:8}}>{tt('presentation_hint')}</div>
            </div>
          </div>
          <div style={{marginTop:16}} className="muted">
            {tt('presentation_points')}
          </div>
        </div>
      </div>
    </Layout>
  );
}

export const getServerSideProps: GetServerSideProps<{ lang: Lang }> = async (ctx) => {
  const lang = getLang(ctx);
  return { props: { lang } };
};
