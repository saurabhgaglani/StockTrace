const TYPE_COLORS = {
  geopolitical: "bg-red-50 text-red-600 border border-red-100",
  supply_chain: "bg-amber-50 text-amber-600 border border-amber-100",
  market_anomaly: "bg-blue-50 text-blue-600 border border-blue-100",
};

function NewsSignalCard({ event, active, onClick }) {
  const badgeClass = TYPE_COLORS[event.event_type] || "bg-gray-100 text-gray-500";
  const ts = new Date(event.timestamp);
  const timeStr = ts.toLocaleTimeString([], { hour: "2-digit", minute: "2-digit" });

  return (
    <button
      onClick={() => onClick(event)}
      className={`w-full text-left px-4 py-3 rounded-2xl border transition-all duration-200
        ${active
          ? "border-[#03fcf8] bg-[#03fcf8]/5 shadow-sm"
          : "border-gray-200 bg-white hover:bg-gray-50 hover:border-gray-300 hover:-translate-y-0.5"
        }`}
    >
      <div className="flex items-start justify-between gap-2 mb-2">
        <span className={`text-[10px] font-semibold px-2 py-0.5 rounded-full ${badgeClass}`}>
          {event.event_type?.replace("_", " ")}
        </span>
        <span className="text-[10px] text-gray-400">{timeStr}</span>
      </div>
      <p className="text-sm text-gray-800 leading-snug font-medium">{event.headline}</p>
      <div className="mt-2 flex items-center gap-2">
        <span className="text-[10px] font-bold px-2 py-0.5 rounded-full bg-gray-100 text-gray-600">
          {event.symbol}
        </span>
        <span className="text-[10px] text-gray-400">{event.source}</span>
        {event.url && (
          <a
            href={event.url}
            target="_blank"
            rel="noopener noreferrer"
            onClick={(e) => e.stopPropagation()}
            className="ml-auto text-[10px] text-[#03fcf8] hover:underline"
          >
            Read →
          </a>
        )}
      </div>
    </button>
  );
}

export default function SignalFeedPanel({ events, activeEvent, onSelect }) {
  return (
    <div className="flex flex-col gap-3">
      <div className="text-xs font-semibold text-gray-400 uppercase tracking-widest px-1">Live Signals</div>
      {events.length === 0 && (
        <div className="text-sm text-gray-400 px-1">Waiting for signals...</div>
      )}
      {events.map((event) => (
        <NewsSignalCard
          key={event.id}
          event={event}
          active={activeEvent?.id === event.id}
          onClick={onSelect}
        />
      ))}
    </div>
  );
}
