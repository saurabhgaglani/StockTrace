import { LineChart, Line, ResponsiveContainer } from "recharts";
import { STOCK_DATA } from "../mockData";

const ITEMS = [
  { ticker: "TSLA" },
  { ticker: "NVDA" },
  { ticker: "AAPL" },
  { ticker: "XOM" },
  { ticker: "BA" },
];

function Sparkline({ series, positive }) {
  const data = series.map((v) => ({ v }));
  return (
    <ResponsiveContainer width={64} height={28}>
      <LineChart data={data}>
        <Line
          type="monotone"
          dataKey="v"
          stroke={positive ? "#00c805" : "#ff5000"}
          strokeWidth={1.5}
          dot={false}
        />
      </LineChart>
    </ResponsiveContainer>
  );
}

export default function WatchlistPanel({ activeSymbol, onSelect }) {
  return (
    <div className="flex flex-col">
      <div className="text-[11px] font-semibold text-gray-400 uppercase tracking-widest px-1 mb-3">Watchlist</div>
      {ITEMS.map(({ ticker }) => {
        const stock = STOCK_DATA[ticker];
        const positive = stock.change >= 0;
        const active = activeSymbol === ticker;
        return (
          <button
            key={ticker}
            onClick={() => onSelect(ticker)}
            className={`w-full text-left px-3 py-3 rounded-xl flex items-center gap-3 transition-all duration-150 mb-1
              ${active ? "bg-gray-100" : "hover:bg-gray-50"}`}
          >
            {/* Active indicator */}
            <div className={`w-0.5 h-8 rounded-full self-stretch ${active ? "bg-[#03fcf8]" : "bg-transparent"}`} />

            <div className="flex-1 min-w-0">
              <div className="flex items-center justify-between">
                <span className="text-sm font-semibold text-gray-900">{stock.name}</span>
                <span className="text-sm font-semibold text-gray-900">${stock.price.toFixed(2)}</span>
              </div>
              <div className="flex items-center justify-between mt-0.5">
                <span className="text-xs text-gray-400">{ticker}</span>
                <span className={`text-xs font-medium ${positive ? "text-[#00c805]" : "text-red-500"}`}>
                  {positive ? "+" : ""}{stock.changePct.toFixed(2)}%
                </span>
              </div>
            </div>

            <Sparkline series={stock.series} positive={positive} />
          </button>
        );
      })}
    </div>
  );
}
