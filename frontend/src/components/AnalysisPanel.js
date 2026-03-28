import { useEffect, useState } from "react";
import { motion, AnimatePresence } from "framer-motion";

const IMPACT_STYLES = {
  high:     "bg-red-50 text-red-600 border-red-100",
  moderate: "bg-amber-50 text-amber-600 border-amber-100",
  low:      "bg-green-50 text-green-600 border-green-100",
};

function TypewriterText({ text }) {
  const [displayed, setDisplayed] = useState("");
  useEffect(() => {
    setDisplayed("");
    if (!text) return;
    let i = 0;
    const id = setInterval(() => {
      setDisplayed(text.slice(0, ++i));
      if (i >= text.length) clearInterval(id);
    }, 16);
    return () => clearInterval(id);
  }, [text]);
  return <span>{displayed}</span>;
}

export default function AnalysisPanel({ analysis, loading, activeEvent, error }) {
  if (!activeEvent && !loading) {
    return (
      <div className="flex flex-col gap-3">
        <div className="text-[11px] font-semibold text-gray-400 uppercase tracking-widest px-1">Agent Insight</div>
        <div className="rounded-2xl border border-gray-200 bg-white px-4 py-8 text-center">
          <p className="text-sm text-gray-400">Select a signal to see AI context</p>
          <p className="text-xs text-gray-300 mt-1">We trace the impact so you don't have to</p>
        </div>
      </div>
    );
  }

  return (
    <div className="flex flex-col gap-3">
      <div className="text-[11px] font-semibold text-gray-400 uppercase tracking-widest px-1">Agent Insight</div>

      {/* Selected signal */}
      {activeEvent && (
        <div className="rounded-xl border border-gray-200 bg-white px-4 py-3">
          <div className="text-[10px] text-gray-400 font-medium uppercase tracking-wide mb-1">Selected Signal</div>
          <p className="text-sm text-gray-800 font-medium leading-snug">{activeEvent.headline}</p>
        </div>
      )}

      {loading && (
        <div className="rounded-xl border border-gray-100 bg-gray-50 px-4 py-4 text-sm font-medium text-gray-400 animate-pulse">
          Analyzing impact…
        </div>
      )}

      {error && !loading && (
        <div className="rounded-xl border border-red-100 bg-red-50 px-4 py-3 text-sm text-red-500">
          {error}
        </div>
      )}

      <AnimatePresence>
        {analysis && !loading && (
          <motion.div key="result" initial={{ opacity: 0, y: 6 }} animate={{ opacity: 1, y: 0 }} className="flex flex-col gap-3">

            {/* Dependency chain */}
            {analysis.path?.length > 0 && (
              <div className="rounded-xl border border-gray-200 bg-white px-4 py-3">
                <div className="text-[10px] text-gray-400 font-medium uppercase tracking-wide mb-2">Traced Impact</div>
                <div className="flex flex-wrap items-center gap-1">
                  {analysis.path.map((node, i) => (
                    <span key={i} className="flex items-center gap-1">
                      <span className="px-2 py-1 rounded-lg bg-gray-100 text-xs text-gray-700 font-medium">{node}</span>
                      {i < analysis.path.length - 1 && <span className="text-gray-300 text-xs">→</span>}
                    </span>
                  ))}
                </div>
              </div>
            )}

            {/* Metrics row */}
            <div className="rounded-xl border border-gray-200 bg-white px-4 py-3">
              <div className="flex items-center justify-between">
                <div>
                  <div className="text-[10px] text-gray-400 font-medium uppercase tracking-wide mb-1">Impact Score</div>
                  <div className="text-2xl font-bold text-gray-900">
                    {Math.round(analysis.impact_score * 100)}
                    <span className="text-sm text-gray-400 font-normal">/100</span>
                  </div>
                </div>
                <span className={`text-xs font-semibold px-3 py-1 rounded-full border ${IMPACT_STYLES[analysis.impact_level] || IMPACT_STYLES.low}`}>
                  {analysis.impact_level?.toUpperCase()}
                </span>
              </div>
              <div className="mt-3 grid grid-cols-2 gap-2 text-xs text-gray-500">
                <div className="bg-gray-50 rounded-lg px-3 py-2">
                  <div className="text-[10px] text-gray-400 mb-0.5">Exposure</div>
                  <div className="font-semibold text-gray-700">Indirect</div>
                </div>
                <div className="bg-gray-50 rounded-lg px-3 py-2">
                  <div className="text-[10px] text-gray-400 mb-0.5">Confidence</div>
                  <div className="font-semibold text-gray-700">{analysis.impact_level === "high" ? "High" : "Moderate"}</div>
                </div>
              </div>
            </div>

            {/* Explanation */}
            <div className="rounded-xl border border-gray-200 bg-white px-4 py-4">
              <div className="text-[10px] text-gray-400 font-medium uppercase tracking-wide mb-2">Context Summary</div>
              <p className="text-sm text-gray-700 leading-relaxed">
                <TypewriterText text={analysis.explanation} />
              </p>
            </div>

            <p className="text-[10px] text-gray-400 px-1 text-center">Context only — not a recommendation.</p>
          </motion.div>
        )}
      </AnimatePresence>
    </div>
  );
}
