import { useState } from "react";
import { LineChart, Line, XAxis, YAxis, Tooltip, ResponsiveContainer } from "recharts";
import { STOCK_DATA } from "../mockData";

const RANGES = ["1D", "1W", "1M", "3M", "1Y"];

const TYPE_COLORS = {
  geopolitical: "bg-red-50 text-red-600",
  supply_chain:  "bg-amber-50 text-amber-600",
  market_anomaly:"bg-blue-50 text-blue-600",
};

const REALTIME_SOURCES = ["gdelt", "finnhub"];

function SignalCard({ event, active, onClick }) {
  const badge = TYPE_COLORS[event.event_type] || "bg-gray-100 text-gray-500";
  const ts = new Date(event.timestamp);
  const timeStr = ts.toLocaleTimeString([], { hour: "2-digit", minute: "2-digit" });
  const isRealtime = REALTIME_SOURCES.includes(event.source);

  return (
    <button
      onClick={() => onClick(event)}
      className={`w-full text-left px-4 py-3 rounded-xl border transition-all duration-150
        ${active
          ? "border-[#03fcf8] bg-[#03fcf8]/5"
          : isRealtime
            ? "border-emerald-200 bg-emerald-50/40 hover:border-emerald-300 hover:-translate-y-px"
            : "border-gray-200 bg-white hover:border-gray-300 hover:-translate-y-px"}`}
    >
      <div className="flex items-center justify-between mb-1.5">
        <div className="flex items-center gap-1.5">
          {isRealtime ? (
            <span className="flex items-center gap-1 text-[10px] font-semibold px-2 py-0.5 rounded-full bg-emerald-100 text-emerald-700 border border-emerald-200">
              <span className="w-1.5 h-1.5 rounded-full bg-emerald-500 animate-pulse inline-block" />
              live
            </span>
          ) : (
            <span className="text-[10px] font-semibold px-2 py-0.5 rounded-full bg-gray-100 text-gray-500 border border-gray-200">
              24h digest
            </span>
          )}
          <span className={`text-[10px] font-semibold px-2 py-0.5 rounded-full ${badge}`}>
            {event.event_type?.replace("_", " ")}
          </span>
        </div>
        <span className="text-[10px] text-gray-400">{timeStr}</span>
      </div>
      <p className="text-sm text-gray-800 font-medium leading-snug">{event.headline}</p>
      <div className="mt-2 flex items-center gap-2">
        <span className="text-[10px] font-bold px-2 py-0.5 rounded-full bg-gray-100 text-gray-500">{event.symbol}</span>
        <span className="text-[10px] text-gray-400">{event.source}</span>
        {event.impact_level && (
          <span className={`text-[10px] font-semibold px-2 py-0.5 rounded-full ${
            event.impact_level === "high"
              ? "bg-red-100 text-red-600"
              : event.impact_level === "moderate"
              ? "bg-amber-100 text-amber-600"
              : "bg-gray-100 text-gray-400"
          }`}>
            {event.impact_level}
          </span>
        )}
        {event.url && (
          <a
            href={event.url}
            target="_blank"
            rel="noopener noreferrer"
            onClick={(e) => e.stopPropagation()}
            className="ml-auto text-[10px] text-[#03fcf8] hover:underline"
          >
            Source →
          </a>
        )}
      </div>
    </button>
  );
}

export default function CenterPanel({ activeSymbol, events, activeEvent, onSelectEvent }) {
  const [range, setRange] = useState("1D");
  const stock = STOCK_DATA[activeSymbol] || STOCK_DATA["TSLA"];
  const positive = stock.change >= 0;
  const chartData = stock.series.map((v, i) => ({ i, v }));

  return (
    <div className="flex flex-col gap-4">
      {/* Stock header */}
      <div className="bg-white rounded-2xl border border-gray-200 px-5 py-4">
        <div className="flex items-start justify-between mb-1">
          <div>
            <h2 className="text-xl font-bold text-gray-900">{stock.name}</h2>
            <span className="text-xs text-gray-400 font-medium">{activeSymbol} · NASDAQ</span>
          </div>
          <div className="text-right">
            <div className="text-2xl font-bold text-gray-900">${stock.price.toFixed(2)}</div>
            <div className={`text-sm font-semibold ${positive ? "text-[#00c805]" : "text-red-500"}`}>
              {positive ? "+" : ""}{stock.change.toFixed(2)} ({positive ? "+" : ""}{stock.changePct.toFixed(2)}%) today
            </div>
          </div>
        </div>

        {/* Chart */}
        <div className="mt-4 h-44">
          <ResponsiveContainer width="100%" height="100%">
            <LineChart data={chartData}>
              <XAxis dataKey="i" hide />
              <YAxis domain={["auto", "auto"]} hide />
              <Tooltip
                contentStyle={{ background: "#fff", border: "1px solid #e5e7eb", borderRadius: 8, fontSize: 12 }}
                formatter={(v) => [`$${v}`, ""]}
                labelFormatter={() => ""}
              />
              <Line
                type="monotone"
                dataKey="v"
                stroke={positive ? "#00c805" : "#ff5000"}
                strokeWidth={2}
                dot={false}
                activeDot={{ r: 4 }}
              />
            </LineChart>
          </ResponsiveContainer>
        </div>

        {/* Range selector */}
        <div className="flex gap-1 mt-3">
          {RANGES.map((r) => (
            <button
              key={r}
              onClick={() => setRange(r)}
              className={`text-xs px-3 py-1 rounded-lg font-medium transition-all duration-100
                ${range === r ? "bg-gray-900 text-white" : "text-gray-500 hover:bg-gray-100"}`}
            >
              {r}
            </button>
          ))}
        </div>
      </div>

      {/* Signal cards */}
      <div className="text-[11px] font-semibold text-gray-400 uppercase tracking-widest px-1">Live Signals</div>
      {events.length === 0 && (
        <p className="text-sm text-gray-400 px-1">Waiting for signals…</p>
      )}
      {events.map((event) => (
        <SignalCard
          key={event.id}
          event={event}
          active={activeEvent?.id === event.id}
          onClick={onSelectEvent}
        />
      ))}
    </div>
  );
}
