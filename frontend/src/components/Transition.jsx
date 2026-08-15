import { useEffect, useState } from "react";
import Logo from "./Logo";

export default function IntroTransition() {
  const [intro, setIntro] = useState(() => {
    return !sessionStorage.getItem("civivos-intro-seen");
  });

  useEffect(() => {
    if (!intro) return undefined;

    const timer = setTimeout(() => {
      sessionStorage.setItem("civivos-intro-seen", "1");
      setIntro(false);
    }, 1250);

    return () => clearTimeout(timer);
  }, [intro]);

  if (!intro) return null;

  return (
    <div className="intro-screen" aria-hidden="true">
      <div className="intro-side-mark">
        <Logo compact />
      </div>
      <div className="intro-line" />
      <div className="intro-wordmark">
        <span>CIVIVOS</span>
        <small>CIVIC OPERATIONS SYSTEM · INDIA</small>
      </div>
      <div className="intro-caption">WORKFLOW FIRST · EVIDENCE ALWAYS</div>
    </div>
  );
}
