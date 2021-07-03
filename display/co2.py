import json

import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import plotly.express as px
import pandas as pd

df = pd.read_csv('./data/population_total.csv')
fig = px.line(df, x= "Year", y="Count", color="Country Name")
fig.update_layout(bargap=0.2)
fig.show()