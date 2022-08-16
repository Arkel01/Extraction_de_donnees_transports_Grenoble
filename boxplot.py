# Script qui affiche le boxplot de la ligne correspondant à la colonne index_of_line_to_plot du csv data_to_load. Les boxplots sont stockés dans le dossier html,
# sous la nomenclature "boxplot_ligne_x.html"

#############################################
data_to_load = 'csv/data_15.08.2022.csv'
index_of_line_to_plot=0
#############################################

import pandas as pd
import plotly.graph_objects as go

df = pd.read_csv(data_to_load, delimiter=';')

vect=[] # Contient une liste par ligne de transport. Chaque liste contient une liste des retards sur chaque arrêt

for line in df['Line'].unique():
    temp=[]
    for direction in df[df['Line']==line]['Direction'].unique():
        for stop in df[(df['Line']==line) & (df['Direction']==direction)]['Stop name'].unique():
            temp.append([list(df[(df['Line']==line)&(df['Direction']==direction)&(df['Stop name']==stop)]['Departure time delay']),
            'Arrêt ' + stop + ' , direction ' + direction]) # append [Retard, Arrêt x direction y]
    vect.append([temp, 'ligne ' + line.split(':')[1]]) # append [[[Retard 1, Arrêt x1 direction y1], [Retard 2, Arrêt x2 direction y2]], ligne z]



fig = go.Figure()
for line in vect[index_of_line_to_plot][0]:
    #fig.add_trace(go.Box(y=k, boxpoints='all', jitter=0.3, pointpos=-1.8)) # Permet d'afficher la série à côté des boxplots
    fig.add_trace(go.Box(y=line[0], name=line[1]))

fig.update_yaxes(range=[-300, 300])
fig.update_layout(
                showlegend=True,
                title="Boxplots des séries des retards de chaque arrêt de la " + vect[index_of_line_to_plot][1],
                yaxis_title="Retard (en secondes)")
fig.update_xaxes(visible=False, showticklabels=False)

fig.write_html('html/boxplot_' + vect[index_of_line_to_plot][1].replace(' ','_') + '.html')
fig.show()