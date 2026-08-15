import { Link, useLocation } from "react-router-dom";
import Logo from "./Logo";
import { LANGUAGES, useI18n } from "../i18n";

export default function Layout({ children }) {
  const location = useLocation();
  const { language, setLanguage, t } = useI18n();
  const lastCaseId = localStorage.getItem("civivos:lastCaseId");

  const nav = [
    ["/", "command"],
    ["/dashboard", "dashboard"],
    ["/new", "newCase"],
  ];

  return (
    <div className="site-shell">
      <aside className="brand-rail">
        <Link to="/" className="brand-link" aria-label="CivivOS home">
          <Logo />
        </Link>
        <div className="brand-rail-meta">INDIA / CIVIC INTELLIGENCE</div>
      </aside>

      <header className="top-nav">
        <div className="nav-spacer" />
        <nav aria-label="Primary navigation">
          {nav.map(([href, key]) => (
            <Link
              key={href}
              to={href}
              className={location.pathname === href ? "nav-active" : ""}
            >
              {t[key]}
            </Link>
          ))}

          {lastCaseId && (
            <>
              <Link
                to={`/case/${lastCaseId}`}
                className={location.pathname === `/case/${lastCaseId}` ? "nav-active" : ""}
              >
                {t.cases}
              </Link>
              <Link
                to={`/case/${lastCaseId}/appeal`}
                className={location.pathname === `/case/${lastCaseId}/appeal` ? "nav-active" : ""}
              >
                {t.appeals}
              </Link>
            </>
          )}
        </nav>

        <div className="nav-right">
          <label className="language-picker" title={t.language}>
            <span>◎</span>
            <select
              value={language}
              onChange={(event) => setLanguage(event.target.value)}
              aria-label={t.language}
            >
              {Object.entries(LANGUAGES).map(([code, name]) => (
                <option key={code} value={code}>{name}</option>
              ))}
            </select>
          </label>
          <div className="nav-meta">
            <span className="live-dot" />
            {t.active}
          </div>
        </div>
      </header>

      <div className="site-content">{children}</div>

      <footer className="site-footer">
        <span>CIVIVOS / CIVIC OPERATIONS SYSTEM</span>
        <span>{t.state} · {t.action} · {t.record}</span>
        <span>{t.india}</span>
      </footer>
    </div>
  );
}
