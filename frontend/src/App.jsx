import { useState } from "react";
import { useAuth0 } from "@auth0/auth0-react";
import Dashboard from "./pages/Dashboard";

function App() {
  const { isLoading, isAuthenticated, loginWithRedirect, logout } = useAuth0();
  const [hoveredBtn, setHoveredBtn] = useState(null);

  if (isLoading) return (
    <div style={s.center}>
      <div style={s.spinner} />
    </div>
  );

  if (!isAuthenticated) return (
    <div style={s.center}>
      <div style={s.loginBox}>
        <div style={s.brand}>
          <div style={s.brandMark}>
            <svg width="16" height="16" viewBox="0 0 16 16" fill="none">
              <circle cx="8" cy="8" r="5" stroke="white" strokeWidth="1.5"/>
              <circle cx="8" cy="8" r="2" fill="white"/>
            </svg>
          </div>
          <div>
            <div style={s.brandName}>NeuroScan</div>
            <div style={s.brandSub}>AI IMAGING</div>
          </div>
        </div>

        <div style={s.divider} />

        <button
          style={{
            ...s.btnPrimary,
            transform: hoveredBtn === "signin" ? "translateY(-2px)" : "translateY(0)",
            boxShadow: hoveredBtn === "signin" ? "0 6px 20px rgba(0,0,0,0.18)" : "none",
            transition: "transform 0.15s ease, box-shadow 0.15s ease",
          }}
          onMouseEnter={() => setHoveredBtn("signin")}
          onMouseLeave={() => setHoveredBtn(null)}
          onClick={() => loginWithRedirect()}
        >
          Sign In
        </button>

        <button
          style={{
            ...s.btnSecondary,
            transform: hoveredBtn === "signup" ? "translateY(-2px)" : "translateY(0)",
            boxShadow: hoveredBtn === "signup" ? "0 6px 20px rgba(0,0,0,0.06)" : "none",
            transition: "transform 0.15s ease, box-shadow 0.15s ease",
          }}
          onMouseEnter={() => setHoveredBtn("signup")}
          onMouseLeave={() => setHoveredBtn(null)}
          onClick={() => loginWithRedirect({ authorizationParams: { screen_hint: "signup" } })}
        >
          Create Account
        </button>
      </div>
    </div>
  );

  return (
    <Dashboard
      logout={() => logout({ logoutParams: { returnTo: window.location.origin } })}
    />
  );
}

const s = {
  center: {
    minHeight: "100vh",
    display: "flex",
    alignItems: "center",
    justifyContent: "center",
    background: "#f4f3f0",
  },
  spinner: {
    width: 28, height: 28, borderRadius: "50%",
    border: "2px solid #e0ddd8",
    borderTop: "2px solid #111",
    animation: "spin 0.8s linear infinite",
  },
  loginBox: {
    background: "#fff",
    borderRadius: 16,
    border: "1px solid #e8e6e0",
    padding: "40px 36px",
    width: 340,
    display: "flex",
    flexDirection: "column",
    gap: 12,
  },
  brand: {
    display: "flex", alignItems: "center",
    gap: 12, marginBottom: 4,
  },
  brandMark: {
    width: 36, height: 36, borderRadius: 10,
    background: "#111", display: "flex",
    alignItems: "center", justifyContent: "center",
    flexShrink: 0,
  },
  brandName: {
    fontSize: 18, fontWeight: 800,
    color: "#111", letterSpacing: "-0.02em",
  },
  brandSub: {
    fontSize: 9, color: "#bbb", letterSpacing: "0.12em",
  },
  divider: {
    height: 1, background: "#e8e6e0", margin: "4px 0",
  },
  btnPrimary: {
    background: "#111", color: "#fff",
    border: "none", borderRadius: 9,
    padding: "13px", fontSize: 13,
    fontWeight: 600, cursor: "pointer",
    letterSpacing: "0.04em",
    fontFamily: "inherit",
  },
  btnSecondary: {
    background: "transparent", color: "#888",
    border: "1px solid #e8e6e0", borderRadius: 9,
    padding: "13px", fontSize: 13,
    cursor: "pointer", fontFamily: "inherit",
  },
};

export default App;