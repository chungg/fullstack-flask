// https://www.chartjs.org/docs/latest/developers/updates.html
function addData(chart, newData, labels) {
  for (const data of newData) {
    chart.data.datasets.push(data);
  }
  if (labels != null) {
    chart.data.labels = labels;
  }
  chart.update();
}

function displayPrices(chart, table, data) {
  const prices = data.indicators.quote[0].close;
  // ideally, should check overlap of labels between datasets
  table.updateOrAddData(data.timestamp.map((a, i) => ({ date: a, [data.meta.symbol]: prices[i] })));
  if (!table.columnManager.columns.length) {
    table.addColumn({ title: "Date", field: "date", frozen: true }, true);
  }
  table.addColumn({
    title: data.meta.symbol,
    field: data.meta.symbol,
    hozAlign: "right",
    headerSort: false,
    formatter: "money",
    formatterParams: { thousand: false },
  });
  chart.data.labels = data.timestamp;
  // change prices to percentage so it's comparable
  chart.data.datasets.push({
    label: data.meta.symbol,
    data: prices.map((x) => ((x - prices[0]) / prices[0]) * 100),
  });
  chart.update();
}

function setupResponseHandlers() {
  document.body.addEventListener("displayPrices", function (evt) {
    const chart = Chart.getChart(evt.detail.target);
    const table = Tabulator.findTable("#priceTable")[0];
    const data = JSON.parse(document.getElementById(evt.detail.dataId).textContent);
    displayPrices(chart, table, data);
    document.getElementById(evt.detail.dataId).remove();
  });

  // chartjs + htmx with payload in HX-Trigger
  document.body.addEventListener("drawChart", function (evt) {
    const chart = Chart.getChart(evt.detail.target);
    // https://www.reddit.com/r/htmx/comments/10sdk43/comment/j72m2j7/
    const data = JSON.parse(document.getElementById(evt.detail.dataId).textContent);
    addData(chart, data.datasets, data.labels);
    document.getElementById(evt.detail.dataId).remove();
  });
}

const isKeyDown = (() => {
  // https://stackoverflow.com/a/48750898
  const state = {};

  // biome-ignore lint: let it mod
  window.addEventListener("keyup", (e) => (state[e.key] = false));
  // biome-ignore lint: let it mod
  window.addEventListener("keydown", (e) => (state[e.key] = true));

  return (key) => (Object.hasOwn(state, key) && state[key]) || false;
})();

export { isKeyDown, setupResponseHandlers };
