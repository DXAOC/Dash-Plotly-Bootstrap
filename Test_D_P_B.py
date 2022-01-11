# git-code full
# https://github.com/Coding-with-Adam/Dash-by-Plotly/blob/master/Bootstrap/Complete_Guide/live_bootstrap.py

import dash
from dash import dcc
from dash import html
from dash.dependencies import Input, Output
import dash_bootstrap_components as dbc
import plotly.express as px
import pandas as pd

df = pd.read_csv('data_house.csv')




app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP],
                meta_tags=[{'name': 'viewport',
                            'content': 'width=device-width, initial-scale=1.0'}]
                )

# Layout section: Bootstrap (https://hackerthemes.com/bootstrap-cheatsheet/)
# ************************************************************************

app.layout = dbc.Container([

    dbc.Row([

        dbc.Col([
            dcc.Dropdown(
                id='graph_dropdown',
                options=[{'label': x, 'value': x} for x in sorted(df['area'].unique())],
                value=['barking and dagenham', 'westminster'],
                multi=True
            ),
            dcc.Graph(id='fig_line', figure={}),
        ],
            xs=12, sm=12, md=12, lg=12, xl=12
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
def update_figure(area_selecter):
    df_area = df[df['area'].isin(area_selecter)]
    figline = px.line(df_area, x='date', y='average_price', color='area')
    return figline


if __name__=='__main__':
    app.run_server(debug=True, port=8000)