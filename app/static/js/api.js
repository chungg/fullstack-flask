function updateChart(evt) {
  const chart = Chart.getChart(evt.detail.target);
  // https://www.reddit.com/r/htmx/comments/10sdk43/comment/j72m2j7/
  const data = JSON.parse(document.getElementById(evt.detail.dataId).textContent);
  for (const dataset of data.datasets) {
    chart.data.datasets.push(dataset);
  }
  if (data.labels != null) {
    chart.data.labels = data.labels;
  }
  chart.update();
  document.getElementById(evt.detail.dataId).remove();
}

function displayPrices(evt) {
  const chart = Chart.getChart(evt.detail.target);
  const table = Tabulator.findTable("#priceTable")[0];
  const data = JSON.parse(document.getElementById(evt.detail.dataId).textContent);
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
  document.getElementById(evt.detail.dataId).remove();
}

export { displayPrices, updateChart };
