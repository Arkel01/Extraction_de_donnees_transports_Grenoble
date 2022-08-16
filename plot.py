# Affiche tous les graphes des retards de chaque ligne, dans chaque station et chaque direction,
# sélectionnable via un menu déroulant. Une zone verte allant d'aucun retard à 1 minute de retard sert de référentiel.
# Le plot est stocké dans le dossier html dans le fichier "plot.html"

import pandas as pd
from datetime import datetime
import pytz
import plotly.graph_objects as go

df = pd.read_csv('csv/data_15.08.2022.csv', delimiter=';')
df = df.drop_duplicates(subset=['Day', 'Line', 'Direction', 'Stop name', 'Stop id', 'Theorical arrival time'], keep='last')

time_column = []
for row in df.iterrows(): # Réécriture des timestamps
    time_column.append(datetime.fromtimestamp(row[1]['Theorical arrival time']).astimezone(pytz.utc).strftime("%m/%d/%Y, %H:%M:%S"))
df.insert(2, "timestamp converted", time_column, True)
df = df.sort_values(by=['timestamp converted'])


# Ajout des boutons du dropdown menu, où le dataframe est filtré
buttons = []
for line in df['Line'].unique():
    for direction in df[df['Line']==line]['Direction'].unique():
        for stop in df[(df['Line']==line) & (df['Direction']==direction)]['Stop name'].unique():
            buttons.append(dict(method='restyle',
                                label= "Ligne " + line.split(':')[1] + ", station " + stop + ", direction " + direction,
                                visible=True,
                                args=[{'x':[df[(df['Line']==line) & (df['Stop name']==stop) & (df['Direction']==direction)]['timestamp converted']],
                                       'y':[df[(df['Line']==line) & (df['Stop name']==stop) & (df['Direction']==direction)]['Departure time delay']],
                                       'type':'scatter'}, [0]],
                                )
                        )

updatemenu = []
your_menu = dict()
updatemenu.append(your_menu)
updatemenu[0]['buttons'] = buttons
updatemenu[0]['direction'] = 'down'
updatemenu[0]['showactive'] = True

fig = go.Figure()

fig.add_trace(go.Scatter(visible=True, mode="lines+markers"))

#fig.add_hline(y=-60,line_dash="dash", line_color="red")
#fig.add_hline(y=60,line_dash="dash", line_color="red")
fig.add_hrect(y0=0, y1=60, line_width=0, fillcolor="green", opacity=0.2)

fig.update_layout(showlegend=False, updatemenus=updatemenu)
fig.update_layout(
    title="Graphe du retard de chaque transport à chaque station en fonction du temps (zone verte : moins d'une minute de retard)",
    xaxis_title="Jour & heure",
    yaxis_title="Retard (en secondes)"
)

fig.write_html('html/plot.html')
fig.show()
