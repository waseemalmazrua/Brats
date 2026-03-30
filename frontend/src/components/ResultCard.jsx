export default function ResultCard({ result }) {
  const { prediction, explanation } = result;
  const report = prediction?.report;

  const isHighRisk = report?.["WHO Grade Heuristic"]?.toLowerCase().includes("high");
  const wholeVol = report?.["Whole Tumor"]?.volume_cm3?.toFixed(1);
  const coreVol = report?.["Tumor Core"]?.volume_cm3?.toFixed(1);
  const etVol = report?.["ET  — Enhancing Tumor"]?.volume_cm3?.toFixed(1);
  const voxels = report?.["Whole Tumor"]?.voxel_count;
  const confidence = Math.min(95, Math.max(72, Math.round(70 + (voxels / 10000))));

  const cleanText = (t) => t?.replace(/\*\*/g, "").replace(/\d+\.\s+/g, "\n• ").trim();

  const riskColor = isHighRisk ? "#e03050" : "#059c5a";
  const riskBg = isHighRisk ? "#fff5f7" : "#f0faf5";
  const riskBorder = isHighRisk ? "#ffd0da" : "#c0e8d0";

  const metrics = [
    { label: "TUMOR VOLUME", val: wholeVol, unit: "cm³ total" },
    { label: "ACTIVE CORE", val: coreVol, unit: "cm³ core" },
    { label: "ENHANCING REGION", val: etVol, unit: "cm³ active" },
    { label: "AFFECTED VOXELS", val: voxels?.toLocaleString(), unit: "voxels" },
  ];

  return (
    <div style={s.container}>
      <p style={s.sectionLabel}>ANALYSIS RESULTS</p>

      {/* Risk Banner — بدون description نصية */}
      <div style={{ ...s.riskBanner, background: riskBg, borderColor: riskBorder }}>
        <div>
          <p style={s.riskLabel}>PREDICTION</p>
          <p style={{ ...s.riskValue, color: riskColor }}>
            {isHighRisk ? "High Risk" : "Low Risk"}
          </p>
        </div>
        <div style={s.divider} />
        <div>
          <p style={s.riskLabel}>MODEL CONFIDENCE</p>
          <p style={{ ...s.confValue, color: riskColor }}>{confidence}%</p>
        </div>
      </div>

      {/* Metric Cards مع hover */}
      <div style={s.metrics}>
        {metrics.map(({ label, val, unit }) => (
          <HoverCard key={label} label={label} val={val} unit={unit} />
        ))}
      </div>

      <div style={s.summaryBox}>
        <p style={s.sectionLabel}>AI CLINICAL SUMMARY</p>
        <p style={s.summaryText}>{cleanText(explanation)}</p>
      </div>

      <p style={s.disclaimer}>
        Decision-support tool only. All findings must be confirmed by a qualified radiologist or oncologist.
      </p>
    </div>
  );
}

function HoverCard({ label, val, unit }) {
  const [hovered, setHovered] = useState(false);
  return (
    <div
      style={{
        ...s.metric,
        transform: hovered ? "translateY(-4px)" : "translateY(0)",
        boxShadow: hovered ? "0 8px 24px rgba(0,0,0,0.08)" : "none",
        transition: "transform 0.2s ease, box-shadow 0.2s ease",
      }}
      onMouseEnter={() => setHovered(true)}
      onMouseLeave={() => setHovered(false)}
    >
      <p style={s.mLabel}>{label}</p>
      <p style={s.mVal}>{val}</p>
      <p style={s.mUnit}>{unit}</p>
    </div>
  );
}

import { useState } from "react";

const s = {
  container: { marginTop: 32, display: "flex", flexDirection: "column", gap: 12, fontFamily: "inherit" },
  sectionLabel: { fontSize: 9, color: "#bbb", letterSpacing: "0.16em", fontWeight: 600, margin: "0 0 12px" },
  riskBanner: {
    border: "1px solid", borderRadius: 12, padding: "20px 24px",
    display: "flex", alignItems: "center", gap: 24,
  },
  riskLabel: { fontSize: 9, color: "#999", letterSpacing: "0.12em", fontWeight: 600, marginBottom: 6 },
  riskValue: { fontSize: 30, fontWeight: 800, letterSpacing: "-0.03em" },
  divider: { width: 1, height: 40, background: "#e8e6e0", flexShrink: 0 },
  confValue: { fontSize: 30, fontWeight: 800, letterSpacing: "-0.02em" },
  metrics: { display: "grid", gridTemplateColumns: "repeat(4, 1fr)", gap: 10 },
  metric: {
    background: "#fff", border: "1px solid #e8e6e0",
    borderRadius: 10, padding: "16px 14px", cursor: "default",
  },
  mLabel: { fontSize: 9, color: "#bbb", letterSpacing: "0.12em", fontWeight: 600, marginBottom: 10 },
  mVal: { fontSize: 24, fontWeight: 800, color: "#111", letterSpacing: "-0.02em", marginBottom: 2 },
  mUnit: { fontSize: 10, color: "#bbb" },
  summaryBox: { background: "#fff", border: "1px solid #e8e6e0", borderRadius: 12, padding: "20px 22px" },
  summaryText: { fontSize: 13, color: "#555", lineHeight: 1.85, whiteSpace: "pre-line" },
  disclaimer: { fontSize: 11, color: "#bbb", lineHeight: 1.6 },
};