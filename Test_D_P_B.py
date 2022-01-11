# https://github.com/Coding-with-Adam/Dash-by-Plotly/blob/master/Bootstrap/Complete_Guide/live_bootstrap.py

import dash
from dash import dcc
from dash import html
from dash.dependencies import Input, Output
import dash_bootstrap_components as dbc
import plotly.express as px
import pandas as pd
from datetime import datetime as dt

df = pd.read_csv('data_house.csv')
df['date'] = pd.to_datetime(df['date'])
df['year'] = df.date.apply(lambda x: x.year)
dff = df.groupby(by=['year', 'area']).mean().reset_index()




app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP],
                meta_tags=[{'name': 'viewport',
                            'content': 'width=device-width, initial-scale=1.0'}]
                )

# Layout section: Bootstrap (https://hackerthemes.com/bootstrap-cheatsheet/)
# ************************************************************************

app.layout = dbc.Container([

    dbc.Row([

        dbc.Col([
            dcc.Graph(id='fig_line', figure={}),
            dcc.Dropdown(
                id='graph_dropdown',
                options=[{'label': x, 'value': x} for x in sorted(df['area'].unique())],
                value=['barking and dagenham', 'westminster'],
                multi=True
            )
        ],
            xs=12, sm=12, md=12, lg=6, xl=6
        ),

        dbc.Col([
            dcc.Graph(id='fig_bar', figure={}),
            dcc.RangeSlider(
                id='range_slider_year',
                marks={i: '{}'.format(i) for i in dff.year},
                min=dff.year.min(),
                max=dff.year.max(),
                value=[dff.year.min()+3, dff.year.min()+6],
                step=1
            )
        ],
        xs=12, sm=12, md=12, lg=6, xl=6
        ),

    ])
])

# Callback section: connecting the components
# ************************************************************************
# Line chart

@app.callback(
    Output('fig_line', 'figure'),
    Input('graph_dropdown', 'value')
)
def update_fig_line(area_selector):
    df_area = df[df['area'].isin(area_selector)]
    fig_line = px.line(df_area, x='date', y='average_price', color='area')
    return fig_line

@app.callback(
    Output('fig_bar', 'figure'),
    Input('range_slider_year', 'value')
)
def update_fig_bar(date_selector):
    #dff = df.groupby(by=['year', 'area']).mean().reset_index()
    dff_date = dff[(dff.year >= date_selector[0]) & (dff.year <= date_selector[1])]
    fig_bar = px.bar(dff_date, x='area', y='no_of_crimes')
    return fig_bar


if __name__=='__main__':
    app.run_server(debug=True, port=8000)


