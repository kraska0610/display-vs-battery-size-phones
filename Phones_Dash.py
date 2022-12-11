"""
creating a dashboard using phone data!
"""

import dash
from dash import dcc
from dash import html
from dash.dependencies import Input, Output
import plotly.express as px
import pandas as pd

stylesheet = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

#pandas dataframe to html table
def generate_table(dataframe, max_rows=200):
    return html.Table([
        html.Thead(
            html.Tr([html.Th(col) for col in dataframe.columns])
        ),
        html.Tbody([
            html.Tr([
                html.Td(dataframe.iloc[i][col]) for col in dataframe.columns
            ]) for i in range(min(len(dataframe), max_rows))
        ])
    ])

app = dash.Dash(__name__, external_stylesheets=stylesheet)
server = app.server


phones = pd.read_csv('/Users/karaska/Desktop/phones_csv')
phones = phones.drop('Unnamed: 0', axis = 1)

    
fig = px.scatter(phones, x='Display Size (inches)', y='Battery (mAh)', color= 'Brand')

app.layout = html.Div([
    html.H1('Relationship Between Display Size and Battery Size for Phones (2020-2022)',
            style={'textAlign' : 'center'}),
    html.H3('Karel Raska: MA 705',
            style={'textAlign' : 'center'}),
    dcc.Graph(figure=fig,
              id='plot',
              style={'width' : '80%',
                     'align-items' : 'center', 'float' : 'right'}),
    html.Div([html.H4('Brands to Display:'),
              dcc.Checklist(
                  options=[{'label': 'Apple', 'value': 'Apple'},
                           {'label': 'Google', 'value': 'Google'},
                           {'label': 'Huawei', 'value': 'Huawei'},
                           {'label': 'LG', 'value': 'LG'},
                           {'label': 'Motorola', 'value': 'Motorola'},
                           {'label': 'Nokia', 'value': 'Nokia'},
                           {'label': 'OnePlus', 'value': 'OnePlus'},
                           {'label': 'Samsung', 'value': 'Samsung'},
                           {'label': 'Sony', 'value': 'Sony'}],
                  value=['Apple', 'Samsung'],
                  id = 'checklist')],
             style={'width' : '20%', 'float' : 'left'}),
    html.Div(id='table'),
    html.Br()   
    ])


@app.callback(
    Output("table", "children"),
    Input("checklist", "value")
)
def update_table(brands):
    x = phones[phones.Brand.isin(brands)].sort_values('Battery (mAh)', ascending = False)
    return generate_table(x)

@app.callback(
    Output("plot", "figure"),
    Input("checklist", "value")
)
def update_plot(brands):
    phones_2 = phones[phones.Brand.isin(brands)]
    fig = px.scatter(phones_2, x='Display Size (inches)', y='Battery (mAh)', color= 'Brand')
    return fig



if __name__ == '__main__':
    app.run_server(debug=True)

