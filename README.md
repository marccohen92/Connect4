# Connect4

An implementation of connect 4 (or more than 4) game with different artificial intelligences (Monte Carlo techniques). The project enables one to play against the AI chosen and also to make play the AI between them. The first goal of the project was to analyse the results of differents contests. This analysis is described below. 

Collaborators :
- AZORIN Raphaël
- COHEN Marc

---------
french version:
## Démarche
Nous avons décidé d’implémenter plusieurs algorithmes Monte-Carlo pour jouer au jeu du Puissance 4. Initialement prévu pour être joué sur une grille 6 x 7, ce jeu a pour but pour chaque joueur d’être le premier à aligner 4 de ses jetons (à la verticale, à l’horizontale ou en diagonale).

Ce jeu à deux joueurs à information complète nous paraissait être un choix logique, notamment pour sa simplicité d’implémentation. Nous avons implémenté le jeu nous même, sans nous inspirer de code existant. 

#### Architecture
Notre projet est découpé de la façon suivante : 
|__ notebooks
	|__ contests.ipynb : notebook faisant jouer les algorithmes les uns contre les autres
	|__ manual_game.ipynb : notebook faisant jouer un humain contre un algorithme
|__ src
	|__ common
		|__ constants.py : constantes pour le jeu et les algorithmes (dimensions, etc.)
	|__ game
		|__ board.py : plateau de jeu
		|__ contest.py : fonction de championnat entre agents, sur plusieurs matchs
		|__ fight.py : fonction de match unique entre agents
		|__ move.py : coups à effectuer sur le plateau de jeu par les joueurs
	|__ intelligences
		|__ flat_mc.py
		|__ ucb.py
		|__ uct.py
		|__ rave.py
		|__ grave.py


Nous avons implémenté différentes méthodes de Monte Carlo pour jouer à ce jeu. L’intérêt principal de ce projet est d’observer les performances des différentes méthodes, ceci en les faisant s’affronter.

Le notebook manual_game.ipynb permet de jouer manuellement contre un de ces algorithmes. Le plateau de jeu est actuellement un tableau Numpy affiché dans le notebook et le joueur humain peut indiquer ses coups via des invites de commandes intégrées.

Pour reproduire nos expérimentations, seul le notebook contests.ipynb est à exécuter. Attention cependant, car il contient déjà les sorties de nos expériences, qui seront alors écrasées. Il sera également nécessaire d’indiquer dans la première cellule de ce notebook contests.ipynb, la localisation du dossier du projet sur votre ordinateur.
Expérimentations
Nous avons effectué les expériences sur un plateau de 7 colonnes, chacune de hauteur 6. Le nombre de jetons à aligner pour gagner est de 4. Ces paramètres sont modifiables dans les constantes du projet. 

## Résultats 
Nous avons fait jouer tous nos algorithmes entre eux, sur une moyenne de 100 matchs avec 1000 playouts. Le joueur qui commence change à chaque match.

#### Flat Monte Carlo
Cet algorithme simple se contente d’effectuer un nombre de playouts (joués de façon aléatoire) depuis un état donné, pour chaque coup. Le coup au gain moyen le plus élevé est ensuite sélectionné.

#### UCB
Algorithme face à UCB : Flat
Win rate d’UCB : 54,5%

Pour cette expérimentation, nous avons exceptionnellement effectué 200 matchs. Comme attendu, notre implémentation d’UCB bat notre implémentation de Flat. Ces résultats sont cohérents. 

#### UCT
Win rate d’UCT face à Flat : 73%
Win rate d’UCT face à UCB : 85%

De même, les performances de notre implémentation d’UCT sont cohérentes car supérieures à celles de Flat et d’UCB.

#### RAVE
Win rate de RAVE face à Flat : 78% (et 3% à égalité)
Win rate de RAVE face à UCB : 74% (et 4% à égalité)
Win rate de RAVE face à UCT : 49% (et 6% à égalité)

Ici, notre implémentation de RAVE n’est pas satisfaisante. Bien que ses performances soient supérieures à celles de Flat et d’UCB comme attendu, RAVE ne parvient pas à battre UCT franchement (49% de victoire et 6% des matchs à égalité). Nous avons expérimenté différents calculs du code AMAF de chaque coup (informations sur la colonne jouée, puis sur la ligne jouée et enfin sur le fait que le coup permette de gagner la partie ou non). Nous obtenons les meilleurs résultats lorsque ce code prend en compte la colonne et la ligne du coup. Selon notre analyse, c’est à cause de ce code AMAF qui n’est pas assez expressif que notre implémentation de RAVE ne parvient pas à vaincre UCT.

#### GRAVE
Win rate de GRAVE face à Flat : 76% (et 4% à égalité)
Win rate de GRAVE face à UCB : 59% (et 2% à égalité)
Win rate de GRAVE face à UCT : 42% (et 8% à égalité)
Win rate de GRAVE face RAVE : 35% (et 8% à égalité)

Ici, les problèmes provenant de notre implémentation de RAVE se reflètent sur celle de GRAVE, qui ne parvient pas non plus à vaincre UCT franchement. De plus, notre implémentation de GRAVE est davantage dégradée et perd face à celle de RAVE.

## Conclusions
Ce projet nous a permis d’implémenter différents algorithmes Monte-Carlo sur un jeu d’apparence simple, que nous avons construit de A à Z.

Nos implémentations de Flat, UCB et UCT affichent des performances satisfaisantes et cohérentes. Cependant, nos RAVE et GRAVE, censés battre les algorithmes précédents, se sont révélés décevants. Avec ce projet, nous avons pris conscience de l’importance de la qualité d’implémentation d’un algorithme de jeu pour pouvoir l’évaluer, aussi bien en termes de gestion de la mémoire qu’en termes de choix conceptuels (hashing, code AMAF, etc.).



