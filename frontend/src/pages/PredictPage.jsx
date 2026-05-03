import { useState } from "react";
import { useAuth0 } from "@auth0/auth0-react";
import ResultCard from "../components/ResultCard";

const BACKEND = import.meta.env.VITE_API_URL;
const KEYS = ["t1", "t1ce", "t2", "flair"];
const LABELS = { t1: "T1", t1ce: "T1CE", t2: "T2", flair: "FLAIR" };

function MedicalLoader({ step }) {
  const steps = [
    { label: "Uploading files to storage", done: step > 0, active: step === 0 },
    { label: "Running AI model", done: step > 1, active: step === 1 },
    { label: "Generating report", done: step > 2, active: step === 2 },
  ];

  return (
    <div style={ls.wrap}>
      <svg width="72" height="72" viewBox="0 0 80 80" fill="none">
        <circle cx="40" cy="40" r="30" stroke="#e8e6e0" strokeWidth="2"/>
        <circle cx="40" cy="40" r="30" stroke="#111" strokeWidth="2"
          strokeDasharray="60 130" strokeLinecap="round"
          style={{ animation: "spin 1.5s linear infinite", transformOrigin: "40px 40px" }}/>
        <circle cx="40" cy="40" r="18" stroke="#e8e6e0" strokeWidth="1.5"/>
        <circle cx="40" cy="40" r="18" stroke="#888" strokeWidth="1.5"
          strokeDasharray="28 85" strokeLinecap="round"
          style={{ animation: "spin 2s linear infinite reverse", transformOrigin: "40px 40px" }}/>
        <circle cx="40" cy="40" r="4" fill="#111"/>
      </svg>

      <div style={ls.steps}>
        {steps.map(({ label, done, active }) => (
          <div key={label} style={ls.step}>
            <div style={{ ...ls.dot, background: done ? "#111" : active ? "#555" : "#e0ddd8" }}/>
            <span style={{ ...ls.stepText, color: done ? "#111" : active ? "#555" : "#ccc" }}>
              {label}
            </span>
            {done && <span style={ls.check}>✓</span>}
          </div>
        ))}
      </div>

      <div style={ls.barTrack}>
        <div style={ls.barFill}/>
      </div>
      <p style={ls.barHint}>This may take 1–2 minutes</p>
    </div>
  );
}

const ls = {
  wrap: {
    background: "#fff", border: "1px solid #e8e6e0",
    borderRadius: 12, padding: "28px 24px",
    display: "flex", flexDirection: "column",
    alignItems: "center", gap: 20, marginBottom: 24,
  },
  steps: { display: "flex", flexDirection: "column", gap: 12, width: "100%", maxWidth: 300 },
  step: { display: "flex", alignItems: "center", gap: 12 },
  dot: { width: 8, height: 8, borderRadius: "50%", flexShrink: 0 },
  stepText: { fontSize: 13, flex: 1 },
  check: { fontSize: 12, color: "#111", fontWeight: 700 },
  barTrack: { width: "100%", height: 3, background: "#f4f3f0", borderRadius: 3, overflow: "hidden" },
  barFill: {
    height: "100%", background: "#111", borderRadius: 3,
    animation: "progress 2s ease-in-out infinite alternate",
  },
  barHint: { fontSize: 11, color: "#bbb" },
};

export default function PredictPage() {
  const { getAccessTokenSilently } = useAuth0();
  const [files, setFiles] = useState({ t1: null, t1ce: null, t2: null, flair: null });
  const [loading, setLoading] = useState(false);
  const [loadingStep, setLoadingStep] = useState(0);
  const [result, setResult] = useState(null);
  const [error, setError] = useState(null);
  const [hoveredCard, setHoveredCard] = useState(null);
  const [drag, setDrag] = useState(null);

  const allReady = KEYS.every((k) => files[k]);
  const remaining = KEYS.filter((k) => !files[k]).length;

  const setFile = (key, file) => {
    if (file) setFiles((p) => ({ ...p, [key]: file }));
  };

  const handleDrop = (key, e) => {
    e.preventDefault(); setDrag(null);
    setFile(key, e.dataTransfer.files[0]);
  };

  const uploadToGCS = async (token, modality, file) => {
    // 1. احصل على signed URL
    const res = await fetch(
      `${BACKEND}/upload/signed-url?filename=${file.name}&modality=${modality}`,
      { headers: { Authorization: `Bearer ${token}` } }
    );
    if (!res.ok) throw new Error("Failed to get signed URL");
    const { url, gcs_path } = await res.json();

    // 2. ارفع الملف مباشرة لـ GCS
    const uploadRes = await fetch(url, {
      method: "PUT",
      body: file,
      headers: { "Content-Type": "application/octet-stream" },
    });
    if (!uploadRes.ok) throw new Error(`Failed to upload ${modality}`);

    return gcs_path;
  };

  const handleSubmit = async () => {
    if (!allReady) return;
    setLoading(true); setError(null); setResult(null); setLoadingStep(0);

    try {
      const token = await getAccessTokenSilently();

      // رفع الملفات لـ GCS
      setLoadingStep(0);
      const gcsPaths = {};
      for (const key of KEYS) {
        gcsPaths[key] = await uploadToGCS(token, key, files[key]);
      }

      // إرسال الـ paths للـ FastAPI
      setLoadingStep(1);
      const res = await fetch(`${BACKEND}/predict/`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          Authorization: `Bearer ${token}`,
        },
        body: JSON.stringify(gcsPaths),
      });

      setLoadingStep(2);
      if (!res.ok) throw new Error(`Prediction failed: ${res.status}`);
      setResult(await res.json());

    } catch (e) {
      setError(e.message);
    } finally {
      setLoading(false);
    }
  };

  const reset = () => {
    setFiles({ t1: null, t1ce: null, t2: null, flair: null });
    setResult(null); setError(null);
  };

  return (
    <div style={s.page}>
      <div style={s.header}>
        <h1 style={s.title}>MRI Analysis</h1>
        <p style={s.sub}>Upload four modality scans to generate AI-powered insights</p>
      </div>

      <p style={s.sectionLabel}>MODALITY FILES</p>
      <div style={s.grid}>
        {KEYS.map((key) => (
          <div
            key={key}
            style={{
              ...s.card,
              borderColor: drag === key ? "#111" : files[key] ? "#111" : "#e8e6e0",
              background: drag === key ? "#f0f0ee" : "#fff",
              transform: hoveredCard === key ? "translateY(-4px)" : "translateY(0)",
              boxShadow: hoveredCard === key ? "0 8px 24px rgba(0,0,0,0.08)" : "none",
            }}
            onDragOver={(e) => { e.preventDefault(); setDrag(key); }}
            onDragLeave={() => setDrag(null)}
            onDrop={(e) => handleDrop(key, e)}
            onMouseEnter={() => setHoveredCard(key)}
            onMouseLeave={() => setHoveredCard(null)}
          >
            <span style={{ ...s.modTag, color: files[key] ? "#111" : "#bbb" }}>
              {LABELS[key]}
            </span>

            <input
              type="file" accept="*/*"
              id={`f-${key}`} style={{ display: "none" }}
              onChange={(e) => setFile(key, e.target.files[0])}
            />

            <label htmlFor={`f-${key}`} style={{
              ...s.selBtn,
              background: files[key] ? "#111" : "#f4f3f0",
              color: files[key] ? "#fff" : "#555",
              borderColor: files[key] ? "#111" : "#e0ddd8",
            }}>
              {files[key] ? "Change" : "Select"}
            </label>

            {files[key]
              ? <span style={s.fileName}>{files[key].name}</span>
              : <span style={s.dropHint}>or drag & drop</span>
            }

            <div style={{
              ...s.pill,
              background: files[key] ? "#111" : "#f8f7f4",
              color: files[key] ? "#fff" : "#ccc",
              borderColor: files[key] ? "#111" : "#e8e6e0",
            }}>
              {files[key] ? "READY" : "PENDING"}
            </div>

            {files[key] && (
              <button style={s.clearBtn}
                onClick={() => setFiles((p) => ({ ...p, [key]: null }))}>
                Clear
              </button>
            )}
          </div>
        ))}
      </div>

      <div style={s.actions}>
        <button
          style={{
            ...s.runBtn,
            opacity: !allReady || loading ? 0.4 : 1,
            cursor: !allReady || loading ? "not-allowed" : "pointer",
          }}
          onClick={handleSubmit}
          disabled={!allReady || loading}
        >
          RUN ANALYSIS
        </button>

        {(result || error) && (
          <button style={s.resetBtn} onClick={reset}>Reset</button>
        )}

        {!allReady && (
          <span style={s.hint}>
            {remaining} file{remaining > 1 ? "s" : ""} remaining
          </span>
        )}
      </div>

      {loading && <MedicalLoader step={loadingStep} />}
      {error && <div style={s.errorBox}>{error}</div>}
      {result && <ResultCard result={result} />}
    </div>
  );
}

const s = {
  page: { maxWidth: 900, fontFamily: "inherit" },
  header: { marginBottom: 32 },
  title: { fontSize: 32, fontWeight: 800, color: "#111", letterSpacing: "-0.03em", margin: "0 0 6px" },
  sub: { fontSize: 13, color: "#999" },
  sectionLabel: { fontSize: 9, color: "#bbb", letterSpacing: "0.16em", fontWeight: 600, margin: "0 0 12px" },
  grid: { display: "grid", gridTemplateColumns: "repeat(4, 1fr)", gap: 10, marginBottom: 20 },
  card: {
    background: "#fff", border: "1px solid",
    borderRadius: 12, padding: "16px 12px",
    display: "flex", flexDirection: "column",
    alignItems: "center", gap: 10,
    transition: "transform 0.2s ease, box-shadow 0.2s ease, border-color 0.15s",
    cursor: "default",
  },
  modTag: { fontSize: 11, letterSpacing: "0.14em", fontWeight: 700 },
  selBtn: {
    border: "1px solid", borderRadius: 7, fontSize: 11,
    padding: "7px 16px", cursor: "pointer",
    fontFamily: "inherit", letterSpacing: "0.04em", fontWeight: 500,
  },
  fileName: { fontSize: 10, color: "#888", textAlign: "center", lineHeight: 1.4, wordBreak: "break-all" },
  dropHint: { fontSize: 10, color: "#ccc" },
  pill: {
    fontSize: 9, padding: "3px 10px", borderRadius: 4,
    border: "1px solid", letterSpacing: "0.12em", fontWeight: 600,
  },
  clearBtn: {
    background: "transparent", border: "1px solid #e8e6e0",
    color: "#ccc", borderRadius: 4, padding: "3px 10px",
    fontSize: 9, cursor: "pointer", fontFamily: "inherit",
  },
  actions: { display: "flex", alignItems: "center", gap: 14, marginBottom: 24 },
  runBtn: {
    background: "#111", color: "#fff", border: "none",
    borderRadius: 9, padding: "13px 36px", fontSize: 12,
    fontWeight: 700, letterSpacing: "0.1em", fontFamily: "inherit",
  },
  resetBtn: {
    background: "transparent", border: "1px solid #e8e6e0",
    color: "#bbb", borderRadius: 9, padding: "13px 20px",
    fontSize: 12, cursor: "pointer", fontFamily: "inherit",
  },
  hint: { fontSize: 11, color: "#bbb" },
  errorBox: {
    background: "#fff5f5", border: "1px solid #ffd0d0",
    color: "#c03030", borderRadius: 8, padding: "12px 16px",
    fontSize: 13, marginBottom: 20,
  },
};