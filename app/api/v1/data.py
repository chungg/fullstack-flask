import json

import flask
from flask import request
import pyarrow.csv as pa_csv
import pyarrow.compute as pc
import numpy as np

from app.api.v1 import bp


@bp.get('/data/random')
def random_data():
    data = {'data': np.random.randint(0, 100, 6).tolist(),
            'label': f'blah{np.random.randint(0, 10000)}'}
    if request.headers.get('Hx-Request'):
        resp = flask.Response()
        resp.headers['HX-Trigger'] = json.dumps(
            {'drawChart': {'target': 'chart_id',
                           'datasets': [data]}})
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
        resp = flask.Response()
        resp.headers['HX-Trigger'] = json.dumps(
            {'drawChart': {'target': 'line_chart_id',
                           **data}})
        return resp
    return data


@bp.get('/data/deaths')
def death_data():
    # https://www150.statcan.gc.ca/n1/daily-quotidien/231127/t001b-eng.htm
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
