# Script qui scrape la ligne line et l'ajoute au csv csv_to_edit. Scrape l'API issue de https://data.mobilites-m.fr/

##########################
line = "SEM:15"
csv_to_edit = 'csv/data.csv'
##########################

import requests
import csv
import os
import time
from datetime import datetime
from datetime import timezone
from threading import Thread

# Scrape la station stops
def scrape_stop(stops, writer):
    info = requests.get("https://data.mobilites-m.fr/api/routers/default/index/stops/{}/stoptimes".format(stops['id']),headers={"origin" : "https://github.com/Arkel01" }).json()
    for elem in info:
        if(line in elem['pattern']['id']):
            for elem2 in elem['times']:
                if (elem2['realtime'] == True):
                    
                    dt = datetime.now() # Timestamp du scrape
                    dt = dt.replace(hour=0, minute=0, second=0, microsecond=0)

                    new_csv_line = [str(datetime.now())[0:10],
                                    line,
                                    elem['pattern']['desc'],
                                    elem2['stopName'],
                                    elem2['stopId'],
                                    int(dt.replace(tzinfo=timezone.utc).timestamp()) + elem2['scheduledArrival'], # Ajout de la date au timestamp de l'heure
                                    elem2['arrivalDelay'],
                                    elem2['departureDelay']
                                    ]
                    if(not any(";".join([str(i) for i in new_csv_line]) in csv_line for csv_line in open(csv_to_edit, 'r', newline='', encoding='utf-8'))):
                        # Si ce retard a déjà été scrape, ne pas l'ajouter à nouveau
                        print(elem2['stopName'])
                        writer.writerow(new_csv_line)

nloop = 10
for k in range(nloop):

    f = open(csv_to_edit, 'a+', newline='', encoding='utf-8')
    writer = csv.writer(f, delimiter =';')

    if os.stat(csv_to_edit).st_size == 0: # Si le csv est vide, ajouter l'entête
        writer.writerow(['Day', 'Line','Direction', 'Stop name', 'Stop id', 'Theorical arrival time', 'Arrival time delay', 'Departure time delay'])

    traj = requests.get("https://data.mobilites-m.fr/api/routers/default/index/routes/{}/stops".format(line)).json()
    for stops in traj:
        if __name__ == '__main__':
            Thread(target = scrape_stop(stops, writer)).start() # Parallélisation des requêtes


    print("Fin du scraping de la ligne.")
    f.close()
    time.sleep(10) # Délai entre les scraping de mise à jour 