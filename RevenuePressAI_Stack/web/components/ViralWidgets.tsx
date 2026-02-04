import Link from 'next/link';
import { t, type Lang } from '../lib/i18n';

export function ViralWidgets({ lang }: { lang: Lang }) {
  const tt = t(lang);
  return (
    <section className="section" style={{marginTop:18}}>
      <div className="grid3">
        <div className="card">
          <div className="h2">{tt('hot_books_title')}</div>
          <p className="muted">{tt('hot_books_copy')}</p>
          <div className="row">
            <span className="badge">#1</span>
            <div>
              <div style={{fontWeight:800}}>{tt('demo_book_1')}</div>
              <div className="muted" style={{fontSize:13}}>{tt('demo_book_1_copy')}</div>
            </div>
          </div>
          <div className="row">
            <span className="badge">#2</span>
            <div>
              <div style={{fontWeight:800}}>{tt('demo_book_2')}</div>
              <div className="muted" style={{fontSize:13}}>{tt('demo_book_2_copy')}</div>
            </div>
          </div>
          <div style={{marginTop:12}}>
            <Link className="link" href="/dashboard">{tt('view_rankings')}</Link>
          </div>
        </div>

        <div className="card">
          <div className="h2">{tt('hot_authors_title')}</div>
          <p className="muted">{tt('hot_authors_copy')}</p>
          <div className="row">
            <span className="badge">▲</span>
            <div>
              <div style={{fontWeight:800}}>{tt('demo_author_1')}</div>
              <div className="muted" style={{fontSize:13}}>{tt('demo_author_1_copy')}</div>
            </div>
          </div>
          <div className="row">
            <span className="badge">★</span>
            <div>
              <div style={{fontWeight:800}}>{tt('demo_author_2')}</div>
              <div className="muted" style={{fontSize:13}}>{tt('demo_author_2_copy')}</div>
            </div>
          </div>
          <div style={{marginTop:12}}>
            <Link className="link" href="/submit">{tt('join_rankings')}</Link>
          </div>
        </div>

        <div className="card">
          <div className="h2">{tt('viral_tools_title')}</div>
          <p className="muted">{tt('viral_tools_copy')}</p>
          <ul className="ul">
            <li>{tt('viral_1')}</li>
            <li>{tt('viral_2')}</li>
            <li>{tt('viral_3')}</li>
            <li>{tt('viral_4')}</li>
          </ul>
        </div>
      </div>
    </section>
  );
}
