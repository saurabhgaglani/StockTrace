const SCENARIOS = [
  { label: "Tesla + Mali",            symbol: "TSLA", headline: "Mining disruption in Mali raises concerns over regional mineral supply",          entities: ["Mali"],        event_type: "geopolitical" },
  { label: "NVIDIA + Export Controls",symbol: "NVDA", headline: "New export controls could affect advanced chip shipments to key markets",          entities: ["Taiwan"],      event_type: "geopolitical" },
  { label: "Apple + Supplier",        symbol: "AAPL", headline: "Manufacturing slowdown in key supplier region sparks delivery concerns",           entities: ["Zhengzhou"],   event_type: "supply_chain" },
  { label: "ExxonMobil + OPEC",       symbol: "XOM",  headline: "OPEC supply signals push energy stocks into focus amid market uncertainty",        entities: ["Middle East"], event_type: "supply_chain" },
];

export default function DemoScenarios({ onTrigger }) {
  return (
    <div className="flex flex-wrap items-center gap-2 mb-5">
      <span className="text-xs text-gray-400 font-medium">Try a scenario:</span>
      {SCENARIOS.map((s) => (
        <button
          key={s.label}
          onClick={() => onTrigger(s)}
          className="text-xs px-3 py-1.5 rounded-full border border-gray-200 bg-white text-gray-600 font-medium hover:border-[#03fcf8] hover:text-gray-900 transition-all duration-150 shadow-sm"
        >
          {s.label}
        </button>
      ))}
    </div>
  );
}
