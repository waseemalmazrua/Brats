import { useState } from "react";

export default function ResultCard({ result }) {
  const { prediction, explanation } = result;
  const report = prediction?.report;

  const wholeVol = report?.["Whole Tumor"]?.volume_cm3?.toFixed(1);
  const coreVol = report?.["Tumor Core"]?.volume_cm3?.toFixed(1);
  const etVol = report?.["ET  — Enhancing Tumor"]?.volume_cm3?.toFixed(1);
  const voxels = report?.["Whole Tumor"]?.voxel_count;

  const cleanText = (t) => t?.replace(/\*\*/g, "").replace(/\d+\.\s+/g, "\n• ").trim();

  const metrics = [
    { label: "TUMOR VOLUME", val: wholeVol, unit: "cm³ total" },
    { label: "ACTIVE CORE", val: coreVol, unit: "cm³ core" },
    { label: "ENHANCING REGION", val: etVol, unit: "cm³ active" },
    { label: "AFFECTED VOXELS", val: voxels?.toLocaleString(), unit: "voxels" },
  ];

  return (
    <div style={s.container}>
      <p style={s.sectionLabel}>ANALYSIS RESULTS</p>

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

const s = {
  container: { marginTop: 32, display: "flex", flexDirection: "column", gap: 12, fontFamily: "inherit" },
  sectionLabel: { fontSize: 9, color: "#bbb", letterSpacing: "0.16em", fontWeight: 600, margin: "0 0 12px" },
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