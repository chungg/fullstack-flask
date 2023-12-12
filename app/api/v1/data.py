import datetime
import json

import flask
from flask import request
import pyarrow.csv as pa_csv
import pyarrow.compute as pc
import numpy as np

from app.api.v1 import bp
from app.extensions import reqs


@bp.get('/data/random')
def random_data():
    label = f'blah{np.random.randint(0, 10000)}'
    data = {'datasets': [{'data': np.random.randint(0, 100, 6).tolist(),
                         'label': label}]}
    if request.headers.get('Hx-Request'):
        resp = flask.Response(
            '<script id="%s" type="application/json">%s</script>' %
            (label, json.dumps(data)))
        resp.headers['HX-Trigger-After-Swap'] = json.dumps(
            {'drawChart': {'target': 'chartId', 'dataId': label}})
        return resp

    return data


@bp.get('/data/sales')
def sales_data():
    # sample processing via duckdb. performance is much worse as of writing
    # df = duckdb.read_csv('app/static/data/Monthly_Transportation_Statistics.csv')
    # table = duckdb.sql("""
    #     SELECT Date, "Light truck sales", "Auto sales",
    #     FROM df
    #     WHERE "Auto sales" is not null
    # """).arrow()

    table = pa_csv.read_csv(
        'app/static/data/Monthly_Transportation_Statistics.csv',
        convert_options=pa_csv.ConvertOptions(timestamp_parsers=['%m/%d/%Y %H:%M:%S %p'])
    ).filter(pc.field('Auto sales').is_valid())
    data = {'datasets': [{'label': 'truck',
                          'data': table['Light truck sales'].to_pylist()},
                         {'label': 'auto',
                          'data': table['Auto sales'].to_pylist()}],
            'labels': pc.strftime(table['Date'], format='%Y-%m-%d').to_pylist()}
    if request.headers.get('Hx-Request'):
        resp = flask.Response(
            '<script id="lineChartData" type="application/json">%s</script>' % (json.dumps(data)))
        resp.headers['HX-Trigger-After-Swap'] = json.dumps(
            {'drawChart': {'target': 'lineChartId', 'dataId': 'lineChartData'}})
        return resp
    return data


@bp.get('/data/deaths')
def death_data():
    table = pa_csv.read_csv('app/static/data/can-deaths.csv')
    data = {'data': table.to_pylist()}
    if request.headers.get('Hx-Request'):
        col_props = ','.join(
          f'{{title:"{col_name}", field:"{col_name}", headerHozAlign:"center", hozAlign:"right"}}'
          for col_name in table.column_names if col_name != 'cause'
        )
        return """
            <script>
              new Tabulator("#death-table", {
                index: "cause",
                layout: "fitColumns",
                data: %s,
                frozenRowsField: "cause",
                frozenRows: ["Total"],
                columnHeaderVertAlign: "bottom",
                columns: [
                  {title: "cause", field: "cause", resizable: "header", frozen: true,
                  },
                  {title: "year",
                   headerHozAlign: "center",
                   columns: [%s]
                  },
                ]
              });
            </script>
        """ % (data['data'], col_props)
    return data


USER_AGENT_HEADERS = {
    # required or yahoo will block
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) '
                  'AppleWebKit/537.36 (KHTML, like Gecko) '
                  'Chrome/39.0.2171.95 Safari/537.36'
}


@bp.get('/data/market/prices')
def get_prices():
    ticker = request.args['ticker']
    interval = request.args.get('interval', '1d')
    start = request.args.get('start', int(datetime.datetime(2023, 1, 1).timestamp()))
    stop = request.args.get('stop', int(datetime.datetime.now().timestamp()))
    events = request.args.get('events', 'capitalGain|div|split')
    res = reqs.session.get(
        f'https://query2.finance.yahoo.com/v8/finance/chart/{ticker}',
        headers=USER_AGENT_HEADERS,
        params={'interval': interval, 'events': events,
                'period1': start, 'period2': stop})
    data = res.json()['chart']['result'][0]
    data['timestamp'] = np.datetime_as_string(
        np.asarray(data['timestamp'], dtype='datetime64[s]'), unit='D').tolist()
    if request.headers.get('Hx-Request'):
        resp = flask.Response()
        resp = flask.Response(
            '<script id="priceData" type="application/json">%s</script>' % (json.dumps(data)))
        resp.headers['HX-Trigger-After-Swap'] = json.dumps(
            {'displayPrices': {'target': 'priceChart', 'dataId': 'priceData'}})
        return resp
    return data
