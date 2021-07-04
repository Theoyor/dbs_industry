from pandas.core.frame import DataFrame
import psycopg2
import decimal
import config
import json

from dash import Dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import plotly.express as px
import pandas as pd
import select_statement as ss


external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = Dash(__name__, external_stylesheets=external_stylesheets)

colors = {
    'background': '#111111',
    'text': '#7FDBFF'
}

conn = None

# read connection parameters

params = config.config()
               # connect to the PostgreSQL server
print('Connecting to the PostgreSQL database...')
conn = psycopg2.connect(**params)
        # create a cursor
cur = conn.cursor()


cur.execute("WITH S AS (SELECT * FROM country_in_year WHERE emission_pp <> 'NaN')                                                                                                  SELECT region, AVG(emission_pp), year_id FROM S, country WHERE S.country_id=country.country_id and region IS NOT NULL GROUP BY S.year_id, region ORDER BY S.year_id ASC              ;")

table = cur.fetchall()

attributes = ["region", "avg", "year_id"]

print("Data collected.")

d = {}
for a in attributes:
    d[a] = []

for row in table:
    for i in range(len(attributes)):
        if isinstance(row[i], decimal.Decimal):
            d[attributes[i]].append(float(row[i]))
        else:
            d[attributes[i]].append(row[i])

df = DataFrame(data=d)

# close the communication with the PostgreSQL
cur.close()

# commit changes
conn.commit()


conn.close()



fig = px.line(df, x= "year_id", y="avg", color="region", title="Co2-emissions per person and year (in tons) by region" )
fig.update_layout(bargap=0.2)
fig.show()

fig.update_layout(
    plot_bgcolor=colors['background'],
    paper_bgcolor=colors['background'],
    font_color=colors['text']
)

