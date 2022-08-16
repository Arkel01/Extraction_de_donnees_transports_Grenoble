# Affiche une carte montrant le retard du transport associé à la ligne line_id à chaque station. 
# Le slider permet de changer l'heure pour constater l'évolution du retard.
# L'objectif du script est de permettre d'afficher un retard pour chaque station quel que soit le timestamp. Etant donné que chaque station fournit
# des timestamps d'heures théoriques différents, il est nécessaire de dupliquer les valeurs du dataframe pour que chaque station possède une donnée
# pour tous les timestamps possibles (sans cela, la carte n'afficherait qu'une station à la fois car dans le cas général, 
# un timestamp d'une station n'est pas commun aux autres stations).
# La carte est stocké dans le dossier html sous la nomenclature "map_ligne_x.html"

##########################
line_id = 'SEM:B'
data_to_load = 'csv/data_15.08.2022.csv'
##########################

import requests
import pandas as pd
from datetime import datetime
import plotly.express as px
import pytz

# Si le retard n'existe pas pour la station stop et le timestamp timestamp, on duplique la ligne du dataframe correspondant
# au retard le plus récent en remplaçant le timestamp
def timestamp_round(stop, line_id, df, timestamp):
    timestamp_list = list(df[
                        (df['Line'] == line_id)
                        & (df['Stop id'] == stop)
                        ]['Theorical arrival time']) # Liste des timestamps de cette station dans cette direction

    timestamp_difference_list = [y - timestamp for y in timestamp_list] # Le plus petit élément positif correspond au retard le plus récent par rapport à timestamp
    closest_existing_timestamp = -1
    for timestamp_difference_element in timestamp_difference_list:
        if timestamp_difference_element > 0:
            if(timestamp_difference_list.index(timestamp_difference_element)-1 == -1): 
                closest_existing_timestamp = timestamp_list[timestamp_difference_list.index(timestamp_difference_element)]
            else:
                closest_existing_timestamp = timestamp_list[timestamp_difference_list.index(timestamp_difference_element)-1]
            break
    if closest_existing_timestamp == -1: # On traite le cas où la station n'a pas encore de retard plus ancien que timestamp
        closest_existing_timestamp = timestamp_list[-1]
    
    closest_df_row = df[
                        (df['Line'] == line_id)
                        & (df['Stop id'] == stop)
                        & (df['Theorical arrival time'] == closest_existing_timestamp)
                        ].iloc[0].tolist() # Nouvelle ligne du dataframe, copie de la valeur la plus récente
    closest_df_row[5] = timestamp
    return(closest_df_row)


df = pd.read_csv(data_to_load, delimiter=';')

df = df[df['Line'] == line_id]

df = df.drop_duplicates(subset=['Day', 'Line', 'Direction', 'Stop name', 'Stop id', 'Theorical arrival time'], keep='last') # Suppression des corrections antérieures pour chaque arrêt
unique_timestamps = df['Theorical arrival time'].unique()

new_df=[]
for stop in df['Stop id'].unique():
    stops_df = df[(df['Stop id']==stop) & (df['Line']==line_id)]
    for timestamp in unique_timestamps:
        current_timestamp_df = stops_df[stops_df['Theorical arrival time'] == timestamp]
        if(len(current_timestamp_df))!=0:
            new_df.append(current_timestamp_df.iloc[0].tolist()) # Si le timestamp correspond à un timestamp de la station stop
        else:
            new_df.append(timestamp_round(stop, line_id, df, timestamp)) # Sinon, dupliquer la valeur la plus récente
new_df = pd.DataFrame(new_df, columns=list(df.columns))


# Création du nouveau dataframe à partir des coordonnées des stations
data=[]
stops = requests.get("https://data.mobilites-m.fr/api/routers/default/index/routes/{}/stops".format(line_id)).json()
for stop in stops:
    for element in new_df[new_df['Stop id'] == stop['id']].iterrows():
        data.append([stop['lat'],
                    stop['lon'],
                    element[1]['Departure time delay'],
                    datetime.fromtimestamp(element[1]['Theorical arrival time']).astimezone(pytz.utc).strftime("%m/%d/%Y, %H:%M:%S")])
df = pd.DataFrame(data, columns=['latitude', 'longitude', 'seconds of delay', 'time'])

df = df.sort_values(by=['time'])

# Tracé des stations
fig1 = px.scatter_mapbox(
    df,
    lat="latitude",
    lon="longitude",
    color="seconds of delay",
    size=[15]*len(df),
    size_max=9,
    animation_frame="time",
    range_color=(-300,300),
    color_continuous_scale=px.colors.diverging.balance,
    color_continuous_midpoint=0,
    center=dict( # Centre de Grenoble
    lat=45.180367,
    lon=5.716656,
    ),
).update_layout(mapbox={"style": "carto-positron", "zoom":12.5}, margin={"l": 0, "r": 0, "t": 50, "b": 0})

fig1.update_layout(
    title="Retard de la ligne " + str(line_id.split(':')[1]) + " à chaque station en fonction du temps",
    yaxis_title="Retard (en secondes)"
)

# Tracé de la ligne
traj = requests.get("https://data.mobilites-m.fr/api/lines/json?types=ligne&codes={}".format(line_id)).json()
coordinates=[]
for coordinate in traj['features'][0]['geometry']['coordinates'][0]:
    coordinates.append([coordinate[1], coordinate[0]])

df = pd.DataFrame(coordinates, columns=['lat', 'lon'])
fig2 = px.line_mapbox(df,
                lat="lat",
                lon="lon",
                zoom=3,
                center=dict(
                lat=45.180367,
                lon=5.716656
                ),
)

fig3 = fig1.add_traces(fig2.data)
fig3.update_traces(line=dict(color="blue", width=1.1))

fig3.write_html('html/map_ligne_' + line_id.split(':')[1] + '.html')
fig3.show()