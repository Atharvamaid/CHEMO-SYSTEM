import numpy as np
import pandas as pd

import plotly
import plotly.express as px

import plotly.graph_objects as go
import plotly.io as pio
from django.contrib.staticfiles import finders


df = pd.read_csv('../CHEMO/covid_19_india.csv', parse_dates=['Date'], dayfirst=True)
df = df[['Date', 'State/UnionTerritory','Cured','Deaths','Confirmed']]
df.columns = ['date', 'state','cured','deaths','confirmed']

today = df[df['date']=='2020-10-27']
confirmed = today.sort_values('confirmed', ascending=True)


#Statewise new confirmed
df['new_confirmed'] = df.groupby(['state'])['confirmed'].diff()
df['new_deaths'] = df.groupby(['state'])['deaths'].diff()
df['new_cured'] = df.groupby(['state'])['cured'].diff()



fig = px.line(df, x="date", y="confirmed", color='state',template= "plotly_white")
fig.update_xaxes(tickfont=dict(family='Rockwell', color='black', size=14))
fig.update_yaxes(tickfont=dict(family='Rockwell', color='black', size=14))
fig.update_traces(mode='lines + markers')
fig.update_layout(legend_orientation="h",legend=dict(x= -.1, y=-.3),
                  autosize=False,
                  width= 650,
                  height= 750,
                  title_text='<b>Confirmed Cases of Covid-19 in India<b> ',
                  title_x=0.5,
                 paper_bgcolor='snow',
                 plot_bgcolor = "snow")



fig1 = px.bar(confirmed, x="confirmed", y="state", orientation='h', text = 'confirmed')
fig1.update_layout(
    title_text='<b>Confirmed cases of Covid-19 per State <b>',
    title_x=0.5,
    paper_bgcolor='whitesmoke',
    plot_bgcolor = "whitesmoke",
    autosize=False,
    width= 850,
    height=750)
fig1.update_traces(marker_color='teal')
fig1.update_xaxes(tickfont=dict(family='Rockwell', color='black', size=14))
fig1.update_yaxes(tickfont=dict(family='Rockwell', color='black', size=14))


deaths = today.sort_values('deaths', ascending=True)
deaths = deaths[deaths.deaths > 0 ]

fig2 = px.bar(deaths, x="deaths", y="state", orientation='h', text = 'deaths')
fig2.update_layout(
    title_text='<b>Deaths due to covid 19<b>',
    title_x=0.5,
    paper_bgcolor='whitesmoke',
    plot_bgcolor = "whitesmoke",
    autosize=False,
    width=850,
    height= 850)
fig2.update_traces(marker_color='#1979e6')
fig2.update_xaxes(tickfont=dict(family='Rockwell', color='darkblue', size=14))
fig2.update_yaxes(tickfont=dict(family='Rockwell', color='darkblue', size=14))


df2 = df.groupby(['date'])[['confirmed', 'deaths','cured',]].sum().reset_index()
df2['new_confirmed'] = df2.confirmed.diff()
df2['new_deaths'] = df2.deaths.diff()
df2['new_cured'] = df2.cured.diff()
#taking dates from 15th March
df2 = df2.iloc[44+75:]

fig3 = go.Figure(go.Bar(x= df2.date, y= df2.cured, name='Recovered'))
fig3.add_trace(go.Bar(x=df2.date, y= df2.deaths, name='Deaths'))
fig3.add_trace(go.Bar(x=df2.date, y= df2.confirmed, name='Confirmed'))

fig3.update_layout(barmode='stack',legend_orientation="h",legend=dict(x= 0.3, y=1.1),
                  xaxis={'categoryorder':'total descending'},
                 title_text='<b>Covid 19 Total cases in India (since 15 March)<b>',
                  title_x=0.5,
                 paper_bgcolor='whitesmoke',
                 plot_bgcolor = "whitesmoke",)
fig3.update_xaxes(tickfont=dict(family='Rockwell', color='black', size=14))
fig3.update_yaxes(tickfont=dict(family='Rockwell', color='black', size=14))



#Forecasting
df3 = df2[['date' , 'confirmed']]
#Renaming column names according to fb prophet
df3.columns = ['ds' , 'y']


#model







