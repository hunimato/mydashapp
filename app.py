#!/usr/bin/env python
# coding: utf-8

# In[ ]:



import dash#the app
from dash import dcc #interactive components
from dash import html#html lags
import plotly.express as px
import pandas as pd
from plotly.subplots import make_subplots
import numpy as np



app = dash.Dash()
# subo las bases
server = app.server
ECH = pd.read_csv('https://raw.githubusercontent.com/hunimato/Dash/main/H_2019_Terceros.csv?token=GHSAT0AAAAAABYEHAE7OH6WV56FW35ULE5GYYL4WIA')


# Construccion 
ECH=ECH.query("nomdpto == 'MONTEVIDEO'")
# create a list of our conditions
conditions = [
    (ECH['HT11'] == 0),
    (ECH['HT11'] <= 50000),
    (ECH['HT11'] <= 100000),
    (ECH['HT11'] > 200000)]

# creo una lista de valores que queremos asignar para cada condicion
values = ['NA','Bajo', 'Medio', 'Alto']

ECH['Nivel_Ingreso'] = np.select(conditions, values)
# display updated DataFrame
#Flights.head()
def Cable_text(numero):
    if numero==1:
        return "Si"
    elif numero==2:
        return "No"
ECH['d21_7'] = ECH['d21_7'].apply(Cable_text)
aux=ECH.groupby(['d21_7','Nivel_Ingreso']).size().sort_values(ascending=False).reset_index(name='n')
aux=aux.sort_values(('Nivel_Ingreso'), ascending=True)
aux = aux.drop(aux[aux.Nivel_Ingreso == '0'].index)
aux = aux.drop(aux[aux.Nivel_Ingreso == 'NA'].index)
fig = px.bar(aux, x="d21_7", y="n", color="Nivel_Ingreso", 
            labels={
                     "d21_7": "Cuentan con Cable",
                     "n": "Cantidad de Hogares"
                 },
            title="Relación entre nivel de ingreso y tenencia de cable.",
            color_discrete_sequence=['#FFD700','#C0C0C0','#8C7853'],
            text_auto=True)
#a_s=aux.sort_values(('Nivel_Ingreso'), ascending=True)

aux=ECH.groupby(['nombarrio'],dropna=True).agg({'d21_7':'count'}).reset_index().rename(columns={'d21_7':'Cable','nombarrio':'Barrio'})
aux=aux.sort_values(('Cable'), ascending=True)

fig2 = make_subplots(rows=4, cols=4)
fig2 = px.scatter(aux,x='Cable', y='Barrio',color="Cable",
                 labels={
                     "Cable": "Cantidad de personas",
                     "Barrio": "Barrio de Montevideo"
                 },
                 size='Cable', hover_data=['Cable'])



fig3 = px.density_heatmap(
    data_frame=aux, x="Cable", y="Barrio",
     labels={
                     "Cable": "Cantidad de personas",
                     "Barrio": "Barrio de Montevideo"
                 },
    color_continuous_scale="darkmint",
title="Grafico de Densidad de poblacion con TV de abonado")
fig3.update_layout(
    autosize=False,
    width=900,
    height=500)



app.layout = html.Div(
    children=[
        html.Div(
            children=[
                html.P(children="📺", className="header-emoji"),
                html.H1(
                    children="ECH Análisis", className="header-title"
                ),
                html.P(
                    children="Aqui visualizaremos los diferentes analisis realizados para nuestra idea",
                    className="header-description",
                ),
            ],
            className="header",
        ),
        html.Div(
            children=[
                html.Div(
                    children=dcc.Graph(
                        id="scatter-chart",
                        config={"displayModeBar": False},
                        figure=fig,
                    ),
                    className="card",
                ),

                html.Div(
                    children=dcc.Graph(
                        id="price-chart",
                        config={"displayModeBar": False},
                        figure=fig2,
                    ),
                    className="card",
                ),

                html.Div(
                    children=dcc.Graph(
                        id="density-chart",
                        config={"displayModeBar": False},
                        figure=fig3,
                    ),
                    className="card",
                ),
                
            ],
            
            className="wrapper",
        ),
    ]
)


if __name__ == "__main__":
    app.run_server(debug=True)

