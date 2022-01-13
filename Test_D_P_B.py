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

    ]),

    dbc.Row([

        dbc.Col([
            dcc.Graph(id='mutlti_fitlter', figure={}),
            dcc.Checklist(
                id='checklist_year',
                options=[{'label': x, 'value': x} for x in sorted(df['year'].unique())],
                value=[dff.year.min(), dff.year.min()+1],
            ),
            dcc.Checklist(
                id='checklist_area',
                options=[{'label': x, 'value': x} for x in sorted(df['area'].unique())],
                value=['barking and dagenham', 'barnet']
            ),
        ],
        xs=12, sm=12, md=12, lg=12, xl=12
        ),
    ]),




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
    dff_date = dff[(dff.year >= date_selector[0]) & (dff.year <= date_selector[1])]
    dff_date['year'] = dff_date['year'].apply(lambda x: str(x))
    fig_bar = px.bar(dff_date, x='area', y='no_of_crimes', color='year')
    return fig_bar

@app.callback(
    Output('mutlti_fitlter', 'figure'),
    [Input('checklist_year', 'value'),
    Input('checklist_area', 'value')]
)
def update_mutlti_fitlter(year, area):
    dff_year_area = dff[(df['area'].isin(area)) & (df['year'].isin(year))]
    fig_year_area = px.bar(dff_year_area, x ='year', y='average_price', color='average_price')
    return fig_year_area


if __name__=='__main__':
    app.run_server(debug=True, port=8000)


