# Extraction de données des transports en commun de la ville de Grenoble
L'objectif de ce petit projet est de mettre en place un algorithme Python permettant de récupérer les données des transports en commun de la ville de Grenoble, dans le but de mettre en évidence de potentielles variations de précision dans les prévisions des heures d'arrivées des transports à chaque station.
<br> 
L'extraction des données repose sur l'API disponible en accès libre à l'adresse suivante :
<p align="center">
https://data.mobilites-m.fr/donnees
</p>

# Visualisation
Les données n'étant disponibles qu'en temps réel, le seul moyen de les récolter est de laisser fonctionner l'algorithme en permanence. On propose donc le jeu de données <code>csv/data_15.08.2022.csv</code>, regroupant les données des tramways **A**, **B** ainsi que de la ligne de bus **15**, sur toute la journée du 15 août 2022. 
<br>
A la fin du scrapping, on obtient un jeu de données ressemblant à ceci :
![Capture d’écran 2022-08-16 151347](https://user-images.githubusercontent.com/14261356/184888390-b8e2a523-dd80-4884-990f-469659a0728a.png)

On propose quelques visualisations permettant de comprendre les données. On utilise pour cela la bibliothèque <code>Plotly</code>, qui nous permet de tracer des graphes interactifs. Ces visualisations seront à la fois proposées en images pour être lisibles directement depuis cette page, mais également en format web pour pouvoir interagir avec celles-ci. On utilisera pour cela le service d'hébergement gratuit www.vercel.com.
<br>

## Cartes
Dans un premier temps, on propose de visualiser les retards sur chaque station en fonction du temps via une carte. Chaque point correspond alors à une station de la ligne observée. Un slider permet de se déplacer dans le temps pour observer l'évolution des valeurs. <code>Plotly</code> hébergeant l'intégralité des données dans le fichier <code>html</code>, la taille du jeu de données peut engendrer des ralentissements en fonction des performances de la machine lors de l'interaction avec le slider, particulièrement si l'on tente de le faire glisser sur un intervalle de temps. On obtient :
<br>
### Ligne A : 
![Capture d’écran 2022-08-16 152151](https://user-images.githubusercontent.com/14261356/184890122-527a5156-eed2-4b98-8f44-6bd75890071c.png)
<p align="center">
https://extraction-de-donnees-transports-grenoble.vercel.app/map_ligne_A.html
</p>

### Ligne B : 
![Capture d’écran 2022-08-16 153153](https://user-images.githubusercontent.com/14261356/184892139-4a5a3d0a-970a-4435-a15a-dd881a555d7e.png)
<p align="center">
https://extraction-de-donnees-transports-grenoble.vercel.app/map_ligne_B.html
</p>

### Ligne 15: 
![Capture d’écran 2022-08-16 152151](https://user-images.githubusercontent.com/14261356/184891313-f2734da8-be95-4dd2-bb9d-2f7865455e20.png)
<p align="center">
https://extraction-de-donnees-transports-grenoble.vercel.app/map_ligne_15.html
</p>


## Courbes

Pour mieux se représenter les variations du retard sur chaque station, on propose une visualisation sous forme de courbe. Dans la version interactive, le menu déroulant permet de sélectionner la station voulue. On choisit arbitrairement un intervalle allant de 0 à 60 secondes de retard, symbolisé par une zone verte sur le graphe, correspondant à un transport "à l'heure". On obtient :
<p align="center">
https://extraction-de-donnees-transports-grenoble.vercel.app/plot.html
</p>
Quelques exemples :

![Capture d’écran 2022-08-16 153730](https://user-images.githubusercontent.com/14261356/184894004-0cc441db-92b5-409f-bf8c-cb7445d014eb.png)
![Capture d’écran 2022-08-16 153743](https://user-images.githubusercontent.com/14261356/184894013-3522e44e-06de-4acc-ac1a-ede4668be215.png)
![Capture d’écran 2022-08-16 153756](https://user-images.githubusercontent.com/14261356/184894022-a5e21d96-d7f1-46db-8af4-4783be3c590e.png)
![Capture d’écran 2022-08-16 153940](https://user-images.githubusercontent.com/14261356/184894026-7c43c376-9f64-4ab3-b7db-8047929704fe.png)

## Boxplots

Enfin, une manière plus concise de se représenter ces nombreuses séries est de les tracer au travers de boxplots. Dans les graphes suivants, les boxplots sont tracés dans l'ordre des stations de la ligne. Comme on peut le constater dans la version interactive, les variations brutales de dispersion des séries correspondent à une nouvelle direction. 

### Ligne A : 
![Capture d’écran 2022-08-16 154447](https://user-images.githubusercontent.com/14261356/184894997-6d0445cd-443a-4b9a-9a6e-2f8105a2d8e8.png)
<p align="center">
https://extraction-de-donnees-transports-grenoble.vercel.app/boxplot_ligne_A.html
</p>

### Ligne B : 
![Capture d’écran 2022-08-16 154530](https://user-images.githubusercontent.com/14261356/184895224-aa95e80b-1da7-4d34-bbce-5847acfb6db4.png)
<p align="center">
https://extraction-de-donnees-transports-grenoble.vercel.app/boxplot_ligne_B.html
</p>

### Ligne 15: 
![Capture d’écran 2022-08-16 154618](https://user-images.githubusercontent.com/14261356/184895338-29259764-2745-49a2-bf85-57b4bf7e86ee.png)
<p align="center">
https://extraction-de-donnees-transports-grenoble.vercel.app/boxplot_ligne_15.html
</p>

## Conclusion

En l'état actuel des choses, au delà des visualisations ci-dessus, il est difficile de tirer des conclusions fiables à partir de ce jeu de données. Pour ce faire, il serait nécessaire d'avoir un jeu de données beaucoup plus important, et étendu dans le temps à toutes les échelles. On pourrait potentiellement constater des variations de retards en fonction du jour de la semaine ou du mois, d'autant plus que plusieurs travaux ont actuellement lieu en août 2022, qui impactent les lignes A et B. 

