import dash
import dash_core_components as dcc
import dash_html_components as html
from dash_html_components.Div import Div
from dash_html_components.Span import Span
import pandas as pd
import plotly.graph_objs as go
import numpy as np
from datetime import datetime, timedelta
import select_statement as sel
import plotly.express as px

def fetch_years():
    df = sel.select(["year_id", "is_snapshot"],["year"], "(year_id % 2) <> 0 AND year_id < 2019")
    df.fillna(0)
    return df

def fetch_data(selector, year):
    #year = 2017
    where = "year_id = {} AND country.country_id = country_in_year.country_id".format(year)
    df = sel.select(["country.country_id", "name", selector],["country", "country_in_year"], where )
    df.fillna(0)
    return(df)

def fetch_sector_data(country_id):
    where = "country_id = \'{}\'".format(country_id)
    df = sel.select(["percentage_agriculture", "percentage_industry", "percentage_service"], ["country"], where)
    df.fillna(0)
    print(df)
    return(df)


external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
app.title = 'Emission-Dash'

years = fetch_years()

app.layout = html.Div(
    [html.Div([
        html.H1("Emissions by country")],
        style={'textAlign': "center", "padding-bottom": "30"}
        ),
    html.Div(
        [html.Span("Metric to display : ", className="six columns",
        style={"text-align": "right", "width": "40%", "padding-top": 10}
        ),
        dcc.Dropdown(
            id="value-selected", value='gdp',
            options=[
                {'label': "Total co2 Emissions ", 'value': 'emission'},
                {'label': "Total GDP ", 'value': 'gdp'},
                ],
            style={"display": "block", "margin-left": "auto","margin-bottom": "5%" , "margin-right": "auto","width": "70%"},
            className="six columns")
            ], 
            className="row"),
        dcc.Slider(
            id='year--slider',
            min=years['year_id'].min(),
            max=years['year_id'].max(),
            value=years['year_id'].max(),
            marks={str(year): str(year) for year in years['year_id'].unique()},
            step=None
        ),

    html.Div(
        [
            dcc.Graph(id="world-map"),
            dcc.Graph(id="pie-chart"),
        ], className="charts", ),
    

    ], 
    className="container")


@app.callback(
    dash.dependencies.Output("pie-chart", "figure"), 
    [dash.dependencies.Input("world-map", "hoverData")])

def generate_chart(country):
    if country == None:
        country = "GER"
    else:
        country = country['points'][0]['location']
    df = fetch_sector_data(country)
    print(df)
    values = list(df.iloc[0])
    fig = px.pie(names= ["agriculture", "industry", "service"], values=values, width= 400) 
    return fig


@app.callback(
    dash.dependencies.Output("world-map", "figure"),
    [
        dash.dependencies.Input("value-selected", "value"),
        dash.dependencies.Input("year--slider", "value")
    ]
)



def update_figure(selected, year):
    # dff = prepare_confirmed_data()

    dff = fetch_data(selected, year)
    dff['hover_text'] = dff["name"] + ": " + dff[selected].apply(str)
    
    bar = {
    "thickness": 10,"len": 0.3,"x": 0.9,"y": 0.7,
    'title': {"text": 'tons pp', "side": "bottom"},
    'tickvals': [ 20, 27],
    'ticktext': ['10,000,000', '10,000,000,000,000']
    }
    
    if selected == "gdp":
        bar["title"] = {"text": 'gdp in $', "side": "bottom"}
        bar["ticktext"] = ['10,000,000', '10,000,000,000,000']
    elif selected == "emission":
        bar["title"] = {"text": 'tons of co2', "side": "bottom"}
        bar["tickvals"] = [20,32]
        bar["ticktext"] = ['10,000,000', '10,000,000,000']


    trace = go.Choropleth(
        locations=dff['country.country_id'],
        z=np.log(dff[selected]),
        text=dff['hover_text'],
        hoverinfo="text",
        marker_line_color='white',
        autocolorscale=False,
        reversescale=True,
        colorscale="hot",
        marker={'line': {'color': '#BBBBBB','width': 0.5}},
        colorbar=bar
    )   
    return {"data": [trace],"layout": go.Layout(  height=600, geo={'showframe': True,'showcoastlines': False,'projection': {'type': "miller"}})}



if __name__ == '__main__':
    app.run_server(debug=True)