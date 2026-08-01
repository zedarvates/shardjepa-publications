# Résumé français : ShardJEPA et les agents incarnés multi-cadence

**Auteur :** Sylvain Galliez
**ORCID :** [https://orcid.org/0009-0009-1286-3683](https://orcid.org/0009-0009-1286-3683)
**Version :** 2026.08.01
**Statut :** Prépublication de dépôt ; non relue par les pairs ; sans DOI

Un agent embarqué contraint ne devrait pas confier perception, contrôle,
sûreté, mémoire, planification et dialogue à un unique modèle de langage. La
thèse proposée est une architecture multi-cadence : chaque décision est routée
vers le composant compétent le moins coûteux, sous budgets explicites de
latence, énergie, mémoire, connectivité et risque. Les petits réseaux, la
mémoire k-NN bornée, les modèles latents et les modèles de langage compacts
peuvent contribuer, mais aucun composant génératif non vérifié ne commande
directement les actionneurs. Une barrière de sûreté indépendante valide chaque
action avant mutation de l'environnement. Cette thèse ne prétend pas que les
LLM sont incapables de fonctionner localement ou de participer à la robotique ;
elle affirme, de façon falsifiable, qu'un routage multi-cadence devrait offrir
un meilleur compromis latence-énergie-mémoire qu'un appel systématique au plus
grand modèle, à réussite et sûreté comparables. ShardJEPA possède déjà certains
contrats nécessaires, mais pas encore la chaîne sensorimotrice, l'ordonnancement
temps réel, les nano-réseaux ou l'orchestration LLM permettant de valider
l'architecture complète. Le Pattern Lab fournit désormais deux vérificateurs
Soroban réellement entraînés, dont un RNN de 961 paramètres qui dépasse la
baseline sans propagation sur des chaînes de retenue/emprunt plus longues.
Cela reste une preuve locale à la tâche, pas un résultat de routage incarné ou
de raisonnement général.
