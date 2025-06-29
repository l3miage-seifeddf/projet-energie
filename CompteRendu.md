# Compte rendu du TP énergie

## Modélisation
1) 
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

2)
On peut proposer une fonction objectif qui agrège les différents objectifs de l'entreprise en utilisant une combinaison
linéaire des deux objectifs. Par exemple, on peut définir la fonction objectif comme suit :
$$
\text{Minimiser } \alpha \cdot \text{Consommation d'énergie} + \beta \cdot \text{Durée totale du planning}
$$
où $\alpha$ et $\beta$ sont des coefficients de pondération qui déterminent l'importance relative de chaque objectif.
On peut ajuster ces coefficients en fonction des priorités de l'entreprise. Par exemple, si l'entreprise accorde plus d'importance à la réduction de la consommation d'énergie, on peut choisir $\alpha$ plus grand que $\beta$. Inversement, si la durée totale du planning est plus critique, on peut choisir $\beta$ plus grand que $\alpha$.

3) 
Pour évaluer une solution réalisable, on peut calculer la consommation d'énergie totale et la durée totale du planning 
en utilisant les variables de décision et les constantes définies précédemment. La consommation d'énergie totale peut 
être calculée en sommant la consommation d'énergie de chaque machine pendant la durée de son utilisation, en tenant 
compte des périodes où elle est allumée et éteinte. La durée totale du planning peut être déterminée en prenant le 
maximum des temps de fin de toutes les opérations.

Pour évaluer une solution non réalisable, on peut attribuer une valeur de pénalité à chaque contrainte violée. 
Par exemple, si une opération dépasse la durée maximale du planning, on peut ajouter une pénalité proportionnelle à
la durée de dépassement. Si l'opération dépasse de 5 unités de temps on applique une pénalité de 5 * le coût par unité 
de temps.


4)
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
1) 
L'algorithme proposé suit le principe suivant : 
Pour chaque opération de chaque job, il évalue toutes les machines,
Il sélectionne immédiatement la machine qui a le coût minimal pour cette opération,
Il attribue définitivement l’opération à cette machine, et ne revient jamais en arrière pour changer ses choix précédents.

Cet algorithme est glouton car il prend à chaque étape la meilleure décision locale, en espérant que cela mène à une solution globale satisfaisante.

2) 

L'algorithme proposé suit le principe suivant : 
Pour chaque opération de chaque job, il évalue toutes les machines,
Il fait ensuite un choix aléatoire parmi les machines disponibles.

Par la suite à chaque exécution, le résultat peut être différent même avec la même instance.

3)
Les deux algorithmes ont une compléxité de O(m*j*o),
m étant le nombre de machines,
j étant le nombre de jobs,
et o étant le nombre d'opérations
On peut dire que les deux compléxités sont **polynomiales**

Nous avons rajouté des tests pour ces heuristiques dans test_constructive.py

## Recherche locale
1) 
#### Première solution de voisinage : changer la machine sur laquelle s'execute une opération 


La taille du voisinage est égale au nombre d'opérations dans la solution multiplié par le nombre de machines disponibles.
On a donc une taille de voisinage de O(O * (M-1)), où o est le nombre d'opérations et m le nombre de machines. 
Le voisinage est de taille polynomiale par rapport à la taille de l'instance.

On peut atteindre toutes les solutions de l'espace de solution en l'utilisant, 
car on peut changer la machine de chaque opération indépendamment des autres. On finira par explorer toutes les
combinaisons possibles de machines pour chaque opération.


#### Deuxième solution de voisinage : Permutations d'ordre sur une machine

Pour chaque machine, si on compte k opérations planifiées sur cette machine, il y a k * (k-1) / 2 
permutations possibles de ces opérations.

On note 
- N = le nombre d'opérations dans la solution 
- M = le nombre de machines

La taille du voisinage est maximum la somme sur toutes les machines des k_i×(k_i-1)/2, 
où k_i est le nombre d’opérations sur la machine i : 

$$
\sum_{i=1}^{m} \frac{k_i (k_i - 1)}{2}
$$


Dans le pire des cas, si toutes les opérations sont sur la même machine,
la taille du voisinage est de O(N^2), où N est le nombre total d'opérations.
Le voisinage est de taille polynomiale par rapport à la taille de l'instance, car il est proportionnel au carré du
nombre d'opérations.

En utilisant uniquement ce voisinage, on ne peut pas atteindre toutes les solutions possibles (on ne peut pas changer 
l’affectation machine d’une opération), mais on peut atteindre toutes les permutations d’ordre pour une affectation 
machine donnée.



2) Nous avons rajouté des tests liés aux voisinnages, et nous avons eu des echecs qui ont ressorti une anomalie
   dans la fonction available_operations.

3) On a implémenté ce qu'on pensait être correct, mais on a eu des échecs dans les tests.
   Nous n'avons pas réussi à tester correctement les voisinages, mais nous pensons être sur le bon chemin.
   Nous avons un problème depuis le début avec la gestion des objets. Etant donné que les objets sont des instances
   de classes, on ne peut pas les comparer directement, et on a du mal à les manipuler. Et aussi certains objets sont 
   donc modifiés et engendrent des effets de bords.

4) Nous avons implémenté un script dans le fichier ```script_test.py``` qui permet en théorie de comparer les solutions
   générées par les heuristiques et les voisinages. 
   Il permet de vérifier si les solutions sont réalisables, et si elles sont différentes.
   Il permet aussi de vérifier si les solutions sont optimales en comparant les valeurs de la fonction objectif.