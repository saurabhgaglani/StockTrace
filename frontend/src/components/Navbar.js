export default function Navbar() {
  return (
    <nav className="fixed top-0 left-0 right-0 z-50 h-14 flex items-center justify-between px-6 bg-white border-b border-gray-200">
      <div className="flex items-center gap-6">
        <span className="text-base font-bold text-gray-900 tracking-tight">StockTrace</span>
        <div className="hidden md:flex items-center gap-1 bg-gray-100 rounded-lg px-3 py-1.5 w-56">
          <svg className="w-3.5 h-3.5 text-gray-400 mr-1.5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M21 21l-4.35-4.35M17 11A6 6 0 1 1 5 11a6 6 0 0 1 12 0z" />
          </svg>
          <span className="text-xs text-gray-400">Search stocks, events…</span>
        </div>
      </div>
      <div className="flex items-center gap-4">
        <div className="flex items-center gap-1.5 text-xs text-gray-500 font-medium">
          <span className="pulse-dot w-1.5 h-1.5 rounded-full inline-block" style={{ backgroundColor: "#03fcf8" }} />
          Agent online
        </div>
        <div className="w-7 h-7 rounded-full bg-gray-900 flex items-center justify-center text-white text-xs font-bold">S</div>
      </div>
    </nav>
  );
}
