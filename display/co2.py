import json

import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import plotly.express as px
import pandas as pd
import select_statement as ss


df = ss.select(["year_id", "country_id", "emission", "population"], ["country_in_year"] )
fig = px.line(df, x= "year_id", y="emission", color="country_id")
fig.update_layout(bargap=0.2)
fig.show()