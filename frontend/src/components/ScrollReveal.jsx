import { useEffect, useRef, useState } from "react";

export default function ScrollReveal({ children, className = "", delay = 0 }) {
  const ref = useRef(null);
  const [state, setState] = useState("before");

  useEffect(() => {
    const node = ref.current;
    if (!node) return undefined;

    const updatePast = () => {
      const rect = node.getBoundingClientRect();
      const viewport = window.innerHeight || 1;
      if (rect.bottom < viewport * 0.24) setState("past");
      else if (rect.top < viewport * 0.82 && rect.bottom > viewport * 0.18) setState("visible");
      else setState("before");
    };

    updatePast();
    window.addEventListener("scroll", updatePast, { passive: true });
    window.addEventListener("resize", updatePast);
    return () => {
      window.removeEventListener("scroll", updatePast);
      window.removeEventListener("resize", updatePast);
    };
  }, []);

  return (
    <section
      ref={ref}
      className={`scroll-scene ${state} ${className}`.trim()}
      style={{ "--scene-delay": `${delay}ms` }}
    >
      {children}
    </section>
  );
}
