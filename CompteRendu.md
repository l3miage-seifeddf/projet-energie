# Compte rendu du TP énergie

## Modélisation
1) Quelles sont les variables de décision ? Quelles sont les contraintes ? Quels sont les objectifs ?

**Les variables de décision** :
- $x_{i,j,m}$ = 1 si l'opération i de la tâche j tourne sur la machine m, 0 sinon
- $y_{m,t}$ = 1 si la machine m est allumée à l'instant t, 0 sinon
- $z_{i,j}$ temps de commencement de l'opération j de la tache i

**Les constantes** :
- Pour chaque opération, sa durée et la quantité d'énergie nécessaire selon de la machine choisie
- Pour chaque machine, sa quantité d'énergie et de temps quand elle est allumée ou éteinte
- Pour chaque machine, sa quantité d'énergie quand elle n'effectue aucune tâche, et quand elle effectue une tâche
- La durée maximale du planning fixée par l'entreprise

**Les contraintes** :
- Une machine sera au moins allumée en début de planning et éteinte en fin de planning
- On doit effectuer les opérations d'une même tâche l'une après l'autre
- Chaque opération doit être assignée à exactement une machine
- Aucune opération ne doit dépasser la durée maximale du planning
- La machine doit être allumée pendant la durée de l'opération

**Les objectifs** : 
- Minimiser la consommation d'énergie
- Minimiser la durée totale du planning

2) **Proposez une fonction objectif qui agrège les différents objectifs de l'entreprise.**

On peut proposer une fonction objectif qui agrège les différents objectifs de l'entreprise en utilisant une combinaison
linéaire des deux objectifs. Par exemple, on peut définir la fonction objectif comme suit :
$$
\text{Minimiser } \alpha \cdot \text{Consommation d'énergie} + \beta \cdot \text{Durée totale du planning}
$$
où $\alpha$ et $\beta$ sont des coefficients de pondération qui déterminent l'importance relative de chaque objectif.
On peut ajuster ces coefficients en fonction des priorités de l'entreprise. Par exemple, si l'entreprise accorde plus d'importance à la réduction de la consommation d'énergie, on peut choisir $\alpha$ plus grand que $\beta$. Inversement, si la durée totale du planning est plus critique, on peut choisir $\beta$ plus grand que $\alpha$.

3) **Comment évaluer (c'est-à-dire donner une valeur à) une solution réalisable ? Comment évaluer une solution non réalisable ?**

Pour évaluer une solution réalisable, on peut calculer la consommation d'énergie totale et la durée totale du planning 
en utilisant les variables de décision et les constantes définies précédemment. La consommation d'énergie totale peut 
être calculée en sommant la consommation d'énergie de chaque machine pendant la durée de son utilisation, en tenant 
compte des périodes où elle est allumée et éteinte. La durée totale du planning peut être déterminée en prenant le 
maximum des temps de fin de toutes les opérations.

Pour évaluer une solution non réalisable, on peut attribuer une valeur de pénalité à chaque contrainte violée. 
Par exemple, si une opération dépasse la durée maximale du planning, on peut ajouter une pénalité proportionnelle à
la durée de dépassement. Si l'opération dépasse de 5 unités de temps on applique une pénalité de 5 * le coût par unité 
de temps.


4) **Proposer une instance pour laquelle il n’existe pas de solution réalisable et expliquer pourquoi aucune solution 
n'est réalisable pour cette instance.**

Une instance pour laquelle il n'existe pas de solution réalisable pourrait être la suivante :
Supposons qu'on ait 1 tâche avec 3 opérations, et 2 machines.
  - Opération 1 : peut se faire sur la **machine 1** en *5 unités de temps*
  - Opération 2 : peut se faire sur la **machine 2** en *10 unités de temps*
  - Opération 3 : peut se faire sur la **machine 1** en *5 unités de temps*

  - Durée maximale du planning : *10 unités de temps*

Sachant que les opérations doivent se faire dans cet ordre : Opération 1 → Opération 2 → Opération 3
Les opérations 1 et 3 ne peuvent se faire que sur la machine 1, et l'opération 2 ne peut se faire que sur la machine 2.
Si on calcule le temps total pour effectuer toutes les opérations, on obtient :
10 unités de temps sur la machine 1 + 10 unités de temps sur la machine 2 (non parallélisable car il y a un ordre
à respecter).
On arrive donc à un temps total de 20 unités de temps, 
ce qui dépasse la durée maximale du planning de 10 unités de temps. L'instance n'est pas réalisable selon nos
contraintes définies.

## Premières heuristiques
1) Proposer un algorithme glouton déterministe qui construit une solution. Préciser en quoi cet algorithme est glouton.
Il sera implémenté dans la classe ```Greedy``` du module ```optim.constructive```.

L'algorithme proposé suit le principe suivant : 
Pour chaque opération de chaque job, il évalue toutes les machines,
Il sélectionne immédiatement la machine qui a le coût minimal pour cette opération,
Il attribue définitivement l’opération à cette machine, et ne revient jamais en arrière pour changer ses choix précédents.

Cet algorithme est glouton car il prend à chaque étape la meilleure décision locale, en espérant que cela mène à une solution globale satisfaisante.

2) Proposer un algorithme non-déterministe qui construit une solution différente pour la même instance à chaque appel.
Il sera implémenté dans la classe ```NonDeterminist``` du module ```optim.constructive```.

L'algorithme proposé suit le principe suivant : 
Pour chaque opération de chaque job, il évalue toutes les machines,
Il fait ensuite un choix aléatoire parmi les machines disponibles.

Par la suite à chaque exécution, le résultat peut être différent même avec la même instance.

3) Pour chacun des algorithmes, indiquer sa complexité.

Les deux algorithmes ont une compléxité de O(m*j*o),
m étant le nombre de machines,
j étant le nombre de jobs,
et o étant le nombre d'opérations

On peut dire que les deux compléxités sont **polynomiales**


## Recherche locale
1) Proposer deux voisinages de solutions. Dans chaque cas, vous indiquerez (en le justifiant)
- la taille du voisinage, 
- si le voisinage est de taille polynomiale par rapport à la taille de l'instance
- si on peut atteindre toutes les solutions de l'espace de solution en l'utilisant
2) Implémenter ces voisinages dans le module ```optim.neighborhoods```.
3) Implémenter dans le module ```optim.local_search``` deux algorithmes de recherche locale.
   Dans les deux cas, la solution initiale sera obtenue par la classe ```NonDeterminist```.
   - Le premier utilisera un seul voisinage et la première solution améliorante pour chaque exploration de voisinage.
   - Le second utilisera les deux voisinages et la meilleure solution de chaque voisinage. Au besoin, on pourra ajouter un critère d'arrêt supplémentaire.
4) Comparer ces deux algorithmes et l'algorithme glouton en termes de temps de calcul et de qualité des solutions obtenues.
   Les algorithmes non-déterministes seront exécutés le même nombre de fois chacun et on gardera la meilleure solution.
   Pour cette question, vous devez implémenter votre propre script et vous pouvez utiliser les instances présentes dans ```data```.