import { useEffect, useState, useCallback } from "react";
import Navbar from "./components/Navbar";
import WatchlistPanel from "./components/WatchlistPanel";
import CenterPanel from "./components/CenterPanel";
import AnalysisPanel from "./components/AnalysisPanel";
import DemoScenarios from "./components/DemoScenarios";
import { fetchEvents, fetchAnalysis, triggerTestEvent } from "./api";

export default function App() {
  const [activeSymbol, setActiveSymbol] = useState("TSLA");
  const [events, setEvents] = useState([]);
  const [activeEvent, setActiveEvent] = useState(null);
  const [analysis, setAnalysis] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  useEffect(() => {
    const load = () => fetchEvents().then(setEvents).catch(() => {});
    load();
    const id = setInterval(load, 30000);
    return () => clearInterval(id);
  }, []);

  const handleSelectEvent = useCallback(async (event) => {
    setActiveEvent(event);
    setAnalysis(null);
    setError(null);
    setLoading(true);
    setActiveSymbol(event.symbol);
    try {
      const result = await fetchAnalysis(event.symbol, event.id);
      setAnalysis(result);
    } catch (e) {
      setError(e.message || "Analysis failed");
    } finally {
      setLoading(false);
    }
  }, []);

  const handleDemoScenario = useCallback(async (scenario) => {
    setLoading(true);
    setAnalysis(null);
    setError(null);
    setActiveSymbol(scenario.symbol);
    try {
      const result = await triggerTestEvent(scenario);
      setActiveEvent(result.event);
      setAnalysis(result);
      fetchEvents().then(setEvents).catch(() => {});
    } catch (e) {
      setError(e.message || "Demo failed");
    } finally {
      setLoading(false);
    }
  }, []);

  const visibleEvents = events.filter((e) => e.symbol === activeSymbol);

  return (
    <div className="min-h-screen bg-[#f7f8fa] text-gray-900">
      <Navbar />
      <div className="pt-14 px-4 pb-10 max-w-7xl mx-auto">
        <div className="py-5">
          <h1 className="text-xl font-bold text-gray-900 mb-0.5">Track what matters. Understand why.</h1>
          <p className="text-sm text-gray-400">From headline to context in seconds — we trace the impact so you don't have to.</p>
        </div>

        <DemoScenarios onTrigger={handleDemoScenario} />

        <div className="grid grid-cols-1 lg:grid-cols-[220px_1fr_320px] gap-4">
          <WatchlistPanel activeSymbol={activeSymbol} onSelect={setActiveSymbol} />
          <CenterPanel
            activeSymbol={activeSymbol}
            events={visibleEvents}
            activeEvent={activeEvent}
            onSelectEvent={handleSelectEvent}
          />
          <AnalysisPanel analysis={analysis} loading={loading} activeEvent={activeEvent} error={error} />
        </div>
      </div>
    </div>
  );
}
