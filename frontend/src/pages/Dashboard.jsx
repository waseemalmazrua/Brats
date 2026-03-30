import { useAuth0 } from "@auth0/auth0-react";
import PredictPage from "./PredictPage";

export default function Dashboard({ logout }) {
  return (
    <div style={s.layout}>
      <aside style={s.sidebar}>
        <div style={s.logo}>
          <div style={s.logoMark}>
            <svg width="16" height="16" viewBox="0 0 16 16" fill="none">
              <circle cx="8" cy="8" r="5" stroke="white" strokeWidth="1.5"/>
              <circle cx="8" cy="8" r="2" fill="white"/>
            </svg>
          </div>
          <div>
            <div style={s.logoText}>NeuroScan</div>
            <div style={s.logoSub}>AI IMAGING</div>
          </div>
        </div>

        <nav style={s.nav}>
          <div style={s.navLabel}>WORKSPACE</div>
          <div style={s.navItem}>
            <div style={s.navDot} />
            Analysis
          </div>
        </nav>

        <button style={s.signOut} onClick={logout}>Sign out</button>
      </aside>

      <main style={s.main}>
        <PredictPage />
      </main>
    </div>
  );
}

const s = {
  layout: {
    display: "flex", minHeight: "100vh",
    background: "#f4f3f0",
    fontFamily: "'Inter', system-ui, sans-serif",
  },
  sidebar: {
    width: 220, background: "#fff",
    borderRight: "1px solid #e8e6e0",
    display: "flex", flexDirection: "column",
    padding: "28px 20px", gap: 24,
  },
  logo: { display: "flex", alignItems: "center", gap: 10 },
  logoMark: {
    width: 32, height: 32, borderRadius: 8,
    background: "#111", display: "flex",
    alignItems: "center", justifyContent: "center", flexShrink: 0,
  },
  logoText: { fontSize: 15, fontWeight: 800, color: "#111", letterSpacing: "-0.02em" },
  logoSub: { fontSize: 9, color: "#bbb", letterSpacing: "0.12em" },
  nav: { flex: 1 },
  navLabel: { fontSize: 9, color: "#bbb", letterSpacing: "0.14em", fontWeight: 600, marginBottom: 8 },
  navItem: {
    display: "flex", alignItems: "center", gap: 10,
    padding: "9px 12px", borderRadius: 8,
    background: "#f4f3f0", color: "#111",
    fontSize: 13, fontWeight: 500, cursor: "pointer",
  },
  navDot: { width: 5, height: 5, borderRadius: "50%", background: "#111", flexShrink: 0 },
  signOut: {
    background: "transparent", color: "#bbb",
    border: "1px solid #e8e6e0", borderRadius: 8,
    padding: "10px", fontSize: 12, cursor: "pointer",
    fontFamily: "inherit", letterSpacing: "0.04em",
  },
  main: { flex: 1, padding: "40px 48px", overflowY: "auto" },
};