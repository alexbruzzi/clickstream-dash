# -*- coding: utf-8 -*-
import dash
from dash.dependencies import Input, Output
import dash_core_components as dcc
import dash_html_components as html
import plotly.figure_factory as ff

from plotly import graph_objs as go
from datetime import datetime as dt
import json
import pandas as pd
import os
from flask import Flask


def make_dash_table(df):
    ''' Return a dash definitio of an HTML table for a Pandas dataframe '''
    table = []
    for index, row in df.iterrows():
        html_row = []
        for i in range(len(row)):
            html_row.append(html.Td([row[i]]))
        table.append(html.Tr(html_row))
    return table


df_task_instance_state_groups = pd.read_json('data/task_instance_state_groups.json').sort_values(by = 'timestamp')
df_redshift_copy = pd.read_json('data/redshift_copy_state.json')
df_task_instance_count_by_day = pd.read_json('data/task_instance_count_by_day.json')

task_instance_data = {}
for state in df_task_instance_state_groups['state'].tolist():
    trace = go.Scatter(
            x = df_task_instance_state_groups[df_task_instance_state_groups['state'] == state]['timestamp'],
            y = df_task_instance_state_groups[df_task_instance_state_groups['state'] == state]['count'],
            name = state,
            opacity = 0.8
    )
    task_instance_data[state] = trace

df_task_instance_count_by_day['d'] = pd.to_datetime(df_task_instance_count_by_day['d'],  unit='ms')
count_by_day = go.Bar(
    x = df_task_instance_count_by_day['d'],
    y = df_task_instance_count_by_day['count'],
    name = 'count_by_day',
    opacity = 0.9
)

df_task_instance_count_by_day['d'] = pd.to_datetime(df_task_instance_count_by_day['d'],  unit='ms')
app = dash.Dash()

app.layout = html.Div([

    html.Div([ # page 1

        html.A([ 'Print PDF' ],
           className="button no-print",
           style=dict(position="absolute", top=-40, right=0)),

        html.Div([ # subpage 1

            # Row 1 (Header)

            html.Div([

                html.Div([
                    html.H5('Astronomer clickXTREME DAG Summary'),
                    html.H6('Another zephyer blows against our house of cards', style=dict(color='#7F90AC')),
                    ], className = "nine columns padded" ),

                html.Div([
                    html.H1([html.Span('07', style=dict(opacity=0.5)), html.Span('13')]),
                    html.H6('Weekly Github Update')
                ], className = "three columns gs-header gs-accent-header padded", style=dict(float='right') ),

            ], className = "row gs-header gs-text-header"),

            html.Br([]),

            # Row 2

            html.Div([

                html.Div([
                    html.H6(["Task Instance Data"],
                            className = "gs-header gs-table-header padded"),
                    dcc.Graph(
                        id='task_instance_data_state_groups',
                        figure={
                            'data':
                                list(task_instance_data.values()),
                            'layout': go.Layout(
                                hovermode='closest',
                                yaxis=dict(
                                    type='log',
                                    autorange=True
                                    )

                            )

                            }
                    )
                ]),

            ]),
            html.Div([
            html.Div([
                    html.H6("Testing a Table"),
                    html.Table(make_dash_table(df_redshift_copy))
                            ]),

                html.Div([
                    html.H6("Something Else", className = "gs-header gs-table-header"),

                    dcc.Graph(
                        id='task_instance_by_day',
                        figure={
                            'data':
                                [count_by_day],
                            'layout': go.Layout(
                                hovermode='closest'
                            )

                            }
                    )


                ],  style=dict(border=0)),

            ], style=dict(border=0)),

        ], ),

    ]),
])

external_css = [ "https://cdnjs.cloudflare.com/ajax/libs/normalize/7.0.0/normalize.min.css",
        "https://cdnjs.cloudflare.com/ajax/libs/skeleton/2.0.4/skeleton.min.css",
        "//fonts.googleapis.com/css?family=Raleway:400,300,600",
        "https://rawgit.com/plotly/dash-app-stylesheets/master/dash-goldman-sachs-report.css",
        "https://maxcdn.bootstrapcdn.com/font-awesome/4.7.0/css/font-awesome.min.css"]

for css in external_css:
    app.css.append_css({ "external_url": css })


if __name__ == '__main__':
    app.run_server(debug=True)
