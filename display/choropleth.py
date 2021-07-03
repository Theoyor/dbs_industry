import dash
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
import plotly.graph_objs as go
import numpy as np
from datetime import datetime, timedelta
import select_statement as sel


def prepare_daily_report():





    current_date = (datetime.today() - timedelta(days=1)).strftime('%m-%d-%Y')

    df = pd.read_csv('./data/test.csv')

    df_country = df.groupby(['Country_Region']).sum().reset_index()
    df_country.replace('US', 'United States', inplace=True)
    df_country.replace(0, 1, inplace=True)
    
    code_df = pd.read_csv('./data/test2.csv')
    df_country_code = df_country.merge(code_df, left_on='Country_Region', right_on='COUNTRY', how='left')

    df_country_code.loc[df_country_code.Country_Region == 'Congo (Kinshasa)', 'CODE'] = 'COD'
    df_country_code.loc[df_country_code.Country_Region == 'Congo (Brazzaville)', 'CODE'] = 'COG'
    
    df = sel.select(["country.country_id", "name", "emission"],["country", "country_in_year"], "year_id = 2017 AND country.country_id = country_in_year.country_id" )
    df.fillna(0)
    return(df)


external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
app.title = 'Covid19-Dash'


app.layout = html.Div([html.Div([html.H1("Emissions by country")],
                                style={'textAlign': "center", "padding-bottom": "30"}
                               ),
                       html.Div([html.Span("Metric to display : ", className="six columns",
                                           style={"text-align": "right", "width": "40%", "padding-top": 10}),
                                 dcc.Dropdown(id="value-selected", value='Confirmed',
                                              options=[{'label': "Confirmed ", 'value': 'Confirmed'},
                                                       {'label': "Recovered ", 'value': 'Recovered'},
                                                       {'label': "Deaths ", 'value': 'Deaths'},
                                                       {'label': "Active ", 'value': 'Active'}],
                                              style={"display": "block", "margin-left": "auto", "margin-right": "auto",
                                                     "width": "70%"},
                                              className="six columns")], className="row"),
                       dcc.Graph(id="my-graph")
                       ], className="container")


@app.callback(
    dash.dependencies.Output("my-graph", "figure"),
    [dash.dependencies.Input("value-selected", "value")]
)

def update_figure(selected):
    # dff = prepare_confirmed_data()

    dff = prepare_daily_report()
    dff['hover_text'] = dff["name"] + ": " + dff["emission"].apply(str)

    trace = go.Choropleth(locations=dff['country.country_id'],
                    	  z=np.log(dff['emission']),
                          text=dff['hover_text'],
                          hoverinfo="text",
                          marker_line_color='white',
                          autocolorscale=False,
                          reversescale=True,
                          colorscale="RdBu",
                          marker={'line': {'color': 'rgb(180,180,180)','width': 0.5}},
                          colorbar={"thickness": 10,"len": 0.3,"x": 0.9,"y": 0.7,
                                    'title': {"text": 'tons', "side": "bottom"},
                                    'tickvals': [ 2, 10],
                                    'ticktext': ['100', '100,000']})   
    return {"data": [trace],
            "layout": go.Layout(height=800,geo={'showframe': False,'showcoastlines': False,'projection': {'type': "miller"}})}

if __name__ == '__main__':
    app.run_server(debug=True)