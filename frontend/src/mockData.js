// Generates a realistic-looking price series for demo purposes
function genSeries(base, points, volatility = 0.012) {
  const data = [];
  let price = base;
  for (let i = 0; i < points; i++) {
    price = price * (1 + (Math.random() - 0.49) * volatility);
    data.push(parseFloat(price.toFixed(2)));
  }
  return data;
}

export const STOCK_DATA = {
  TSLA: { name: "Tesla",      price: 214.81, change: +2.34, changePct: +1.10, series: genSeries(210, 60) },
  NVDA: { name: "NVIDIA",     price: 875.40, change: -8.20, changePct: -0.93, series: genSeries(880, 60) },
  AAPL: { name: "Apple",      price: 189.30, change: +0.87, changePct: +0.46, series: genSeries(187, 60) },
  XOM:  { name: "ExxonMobil", price: 118.55, change: +1.92, changePct: +1.65, series: genSeries(116, 60) },
  BA:   { name: "Boeing",     price: 172.10, change: -3.45, changePct: -1.97, series: genSeries(175, 60) },
};
