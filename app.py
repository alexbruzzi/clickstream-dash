# -*- coding: utf-8 -*-
import dash
from dash.dependencies import Input, Output
import dash_core_components as dcc
import dash_html_components as html

from plotly import graph_objs as go
from datetime import datetime as dt
import json
import pandas as pd
import os
from flask import Flask

df = pd.read_json('data.json').sort_values(by = 'timestamp')

data = {}
for state in df['state'].tolist():
    trace = go.Scatter(
            x = df[df['state'] == state]['timestamp'],
            y = df[df['state'] == state]['count'],
            name = state,
            opacity = 0.8
    )
    data[state] = trace

app = dash.Dash()
app.layout = html.Div(children=[
    html.H1(children='clickXTREME'),

    html.Div(children='''
        Ain't this some shit.
    '''),

    dcc.Graph(
        id='sample_one',
        figure={
            'data':
                list(data.values()),
            'layout': go.Layout(
                hovermode='closest',
                yaxis=dict(
                    type='log',
                    autorange=True
                    )

            )

            }
)
])

if __name__ == '__main__':
    app.run_server(debug=True)
