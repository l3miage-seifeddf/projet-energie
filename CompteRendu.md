# Compte rendu du TP énergie

## Modélisation
1) Quelles sont les variables de décision ? Quelles sont les contraintes ? Quels sont les objectifs ?
Les variables de décision sont:
- $x_{i,j,m}$ = 1 si l'opération i de la tâche j tourne sur la machine m, 0 sinon
- $y_{m,t}$ = 1 si la machine m est allumée à l'instant t, 0 sinon
- $z_{i,j}$ temps de commencement de l'opération j de la tache i
Les constantes sont:
- Pour chaque opération, sa durée et la quantité d'énergie nécessaire selon de la machine choisie
- Pour chaque machine, sa quantité d'énergie et de temps quand elle est allumée ou éteinte
- Pour chaque machine, sa quantité d'énergie quand elle n'effectue aucune tâche, et quand elle effectue une tâche
- La durée maximale du planning fixée par l'entreprise
Les contraintes:
- Une machine sera au moins allumée en début de planning et éteinte en fin de planning
- On doit effectuer les opérations d'une même tâche l'une après l'autre
- Chaque opération doit être assignée à exactement une machine
- Aucune opération ne doit dépasser la durée maximale du planning
- La machine doit être allumée pendant la durée de l'opération