import { Link } from "react-router-dom";
import CivicArtifact from "../components/CivicArtifact";
import ScrollReveal from "../components/ScrollReveal";
import { useI18n } from "../i18n";

export default function Home() {
  const lastCaseId = localStorage.getItem("civivos:lastCaseId");
  const { t } = useI18n();

  return (
    <main>
      <section className="home-hero hero-scene">
        <div className="hero-photo" aria-hidden="true" />
        <div className="hero-overlay" aria-hidden="true" />

        <div className="hero-copy">
          <p className="eyebrow">{t.heroEyebrow}</p>
          <h1>
            {t.heroTitle1}<br />
            {t.heroTitle2}<br />
            <em>{t.heroTitle3}</em>
          </h1>
          <p className="hero-lead">{t.heroLead}</p>
          <div className="hero-rule" />
          <div className="hero-foot">{t.workflowFirst}</div>
          <div className="hero-actions">
            <Link className="ink-button" to="/new">
              {t.startCase}<span>↗</span>
            </Link>
            {lastCaseId && (
              <Link className="quiet-link" to={`/case/${lastCaseId}`}>
                {t.continueCase}
              </Link>
            )}
          </div>
        </div>

        <div className="hero-art-wrap">
          <CivicArtifact />
          <div className="system-monitor">
            <div className="monitor-top"><span>{t.monitor}</span><i /></div>
            <strong>CASE ENGINE</strong>
            <p>{t.monitorText}</p>
            <div className="monitor-states">
              <span>ANALYZE</span><span>DRAFT</span><span>WATCH</span><span>ESCALATE</span>
            </div>
          </div>
        </div>
      </section>

      <ScrollReveal className="statement-section" delay={50}>
        <p className="eyebrow">{t.principle}</p>
        <div className="statement-grid">
          <h2>{t.principleTitle}</h2>
          <p>{t.principleText}</p>
        </div>
      </ScrollReveal>

      <ScrollReveal className="workflow-section" delay={90}>
        <div className="section-head">
          <div><p className="eyebrow">{t.how}</p><h2>{t.howTitle}</h2></div>
          <p>{t.howText}</p>
        </div>
        <div className="workflow-grid">
          {t.steps.map((step, i) => (
            <div className="workflow-card" key={`${step}-${i}`}>
              <span>0{i + 1}</span>
              <div><strong>{step}</strong><small>{["INPUT","REASONING","ROUTE","DOCUMENT","WATCHER","ESCALATION"][i]}</small></div>
            </div>
          ))}
        </div>
      </ScrollReveal>

      <ScrollReveal className="dark-manifesto" delay={110}>
        <div>
          <p className="eyebrow dark-eyebrow">{t.intelligence}</p>
          <h2>{t.intelligenceTitle}</h2>
          <p className="dark-lead">{t.intelligenceText}</p>
        </div>
        <div className="manifesto-grid">
          {t.steps.slice(0, 4).map((step, i) => (
            <div key={step}><span>0{i + 1}</span><p>{step}</p></div>
          ))}
        </div>
      </ScrollReveal>
    </main>
  );
}
