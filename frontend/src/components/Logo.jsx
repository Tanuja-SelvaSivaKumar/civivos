export default function Logo({ compact = false }) {
  return <div className={`logo-lockup ${compact?'logo-compact':''}`}>
    <svg className="logo-mark" viewBox="0 0 72 72" aria-hidden="true">
      <path d="M46 11c-6-5-16-6-24-2C11 14 5 25 6 37c1 13 10 23 22 25 10 2 19-1 25-8l-5-6c-5 5-11 7-18 6-9-1-16-8-17-18-1-9 3-18 11-22 7-3 15-2 20 3l7-6Z" fill="currentColor"/>
      <circle cx="36" cy="22" r="4" fill="currentColor"/><rect x="24" y="30" width="24" height="4" rx="2" fill="currentColor"/>
      <rect x="27" y="38" width="4" height="19" fill="currentColor"/><rect x="34" y="38" width="4" height="19" fill="currentColor"/><rect x="41" y="38" width="4" height="19" fill="currentColor"/>
    </svg>
    <div className="logo-type"><span>CivivOS</span>{!compact&&<small>Civic Operations System</small>}</div>
  </div>;
}