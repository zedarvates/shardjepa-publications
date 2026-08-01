# ShardJEPA et les agents incarnés multi-cadence sous contraintes de ressources

**Auteur :** Sylvain Galliez
**ORCID :** [https://orcid.org/0009-0009-1286-3683](https://orcid.org/0009-0009-1286-3683)
**Version :** 2026.08.01
**Statut :** Prépublication de dépôt ; non relue par les pairs ; sans DOI
**Licence :** CC BY 4.0

**Manuscrit canonique anglais :** [`paper.md`](paper.md)

## Résumé

Un agent incarné soumis à des limites de mémoire, d'énergie et de latence ne
devrait pas confier perception, contrôle, sûreté, mémoire, planification et
dialogue à un unique modèle de langage. Nous proposons une architecture
multi-cadence dans laquelle chaque décision est routée vers le composant
compétent le moins coûteux, sous budgets explicites de latence, d'énergie, de
mémoire, de connectivité et de risque. Les micro-réseaux, la récupération k-NN,
les modèles latents et les modèles de langage compacts peuvent tous contribuer,
mais aucun composant génératif non vérifié ne contrôle directement les
actionneurs. Une couche indépendante d'assurance à l'exécution vérifie chaque
action avant toute mutation de l'environnement. La thèse est volontairement
plus étroite que l'affirmation selon laquelle les LLM seraient incapables de
fonctionner localement ou de participer à la robotique : des modèles compacts,
des techniques d'inférence sous contrainte mémoire et des systèmes
vision-langage-action constituent déjà des contre-exemples. L'hypothèse
scientifique est donc comparative et falsifiable : à réussite et sûreté
équivalentes, le routage multi-cadence devrait améliorer le front de Pareto
latence-énergie-mémoire par rapport à l'appel systématique au plus grand modèle.
Le Pattern Lab ajoute désormais deux petits experts réellement entraînés, mais
ils ne valident pas encore le routage d'un agent incarné.

## 1. Thèse centrale corrigée

La formulation défendable est la suivante :

> Un agent incarné sous contraintes devrait utiliser le modèle de langage comme
> composant délibératif optionnel et non souverain. Le contrôle rapide, la
> validation des actions, la mémoire bornée et la reprise après défaillance
> doivent rester locaux, explicitement budgétés et testables indépendamment.

Cette thèse ne dit pas que les LLM n'ont aucun avenir dans les agents
autonomes. Elle dit qu'ils ne devraient être ni l'unique substrat de calcul, ni
l'autorité finale sur l'action physique.

Les travaux MobileLLM montrent l'existence de modèles sous le milliard de
paramètres adaptés à des usages locaux [2]. *LLM in a Flash* montre qu'une
inférence contrainte par la DRAM peut exploiter le stockage flash [3]. Mamba
montre que le traitement séquentiel utile ne se limite pas à l'attention dense
quadratique [4]. SayCan combine planification langagière et affordances [6],
tandis que RT-2 étudie directement le contrôle robotique vision-langage-action
[7]. Ces résultats invalident les formulations universelles comme « un LLM ne
peut pas fonctionner localement » ou « un LLM ne peut pas agir en robotique ».

Ils ne suppriment pas pour autant les contraintes d'un système incarné :
échéances, sûreté, état partiellement observable, consommation, modes dégradés
et validation de l'action.

## 2. Ce qui devait être corrigé

| Formulation initiale | Formulation publiable |
|---|---|
| Les LLM font nécessairement 10–70 milliards de paramètres | De nombreux modèles de pointe sont grands, mais des modèles locaux sous le milliard de paramètres existent. |
| L'attention est toujours quadratique | L'attention complète l'est par rapport à la longueur de séquence, mais les fenêtres glissantes, la parcimonie, les récurrences et les SSM modifient ce coût. |
| Une couche locale produit zéro hallucination | Un composant étroit et déterministe réduit certaines erreurs génératives ; il ne garantit pas la justesse sémantique. |
| Le déterminisme garantit la sûreté | La répétabilité ne remplace ni une spécification de sûreté, ni une surveillance indépendante, ni un mode de repli. |
| Le k-NN s'adapte gratuitement et instantanément | L'insertion est simple, mais mémoire et temps de recherche augmentent avec les données retenues. |
| Les micro-réseaux remplaceront 80 % des décisions | C'est une hypothèse expérimentale ; aucun résultat ShardJEPA ne démontre ce pourcentage. |
| Tous les robots doivent rester sous 1–3 W et 1–4 Go | Chaque appareil et chaque mission possèdent leur propre enveloppe, qui doit être mesurée. |
| L'architecture multi-échelle est la seule viable | C'est une architecture candidate à comparer aux contrôleurs classiques, aux systèmes hybrides et aux modèles VLA de bout en bout. |

Le terme initial **GEPA** désignait ici une « Generalized Embedded Perception
Architecture ». Il entre désormais en collision avec GEPA, un optimiseur de
prompts Genetic-Pareto publié [9]. Le présent texte emploie donc **plan local de
perception et d'action** (*Local Perception and Action Plane*, LPAP).

## 3. Modèle de ressources

Le profil d'un déploiement est décrit par

\[
\mathcal{B}=(M_{max},P_{avg},E_{mission},D_{control},D_{task},C_{net}),
\]

où figurent la mémoire maximale, la puissance moyenne, l'énergie de mission,
les échéances de contrôle et de tâche, ainsi que le contrat de connectivité.
Ces valeurs sont des mesures propres au matériel et à la mission.

Pour chaque module candidat \(j\), le routeur estime latence \(L_j\), énergie
\(E_j\), mémoire \(M_j\), risque \(R_j\) et utilité attendue \(Q_j\). Un module
n'est admissible que s'il respecte tous les budgets. Parmi les modules
admissibles, le routeur maximise l'utilité pénalisée par les coûts. Si aucun
module n'est admissible, le système choisit un mode sûr ou dégradé défini à
l'avance ; il ne lance pas une escalade non bornée.

## 4. Architecture multi-cadence proposée

| Niveau | Responsabilité | Mécanismes candidats | Autorité |
|---|---|---|---|
| L0 | Assurance à l'exécution et repli sûr | gardes vérifiées, contrôleurs classiques, arrêt d'urgence | peut bloquer ou remplacer toute action |
| L1 | Conditionnement du signal et réflexes | filtres, seuils, automates, nano-politiques proposées | local et strictement borné |
| L2 | Évaluation apprise rapide | micro-MLP ShardJEPA, petits CNN/RNN/SSM, détecteurs d'anomalies | produit scores ou actions bornées |
| L3 | Plan local de perception et d'action | fusion de capteurs, extraction de caractéristiques, routage de capacités | génère des propositions locales |
| L4 | Mémoire épisodique et planification latente | k-NN borné, prédiction latente, recherche bornée | propose un plan sous budget |
| L5 | Délibération langagière locale | petit modèle de langage, planificateur structuré, dialogue | consultatif, sans mutation directe |
| L6 | Délibération distante optionnelle | modèle cloud langagier ou multimodal | consultatif et dépendant du réseau |

Tous les niveaux ne sont pas obligatoires. Un petit robot peut fonctionner sans
modèle de langage. Un agent conversationnel mobile peut employer souvent L5,
tout en conservant une barrière L0 indépendante.

## 5. Invariant de sûreté

La politique \(\pi\) propose une action \(\hat a_t\) depuis l'observation
\(o_t\). L'environnement ne peut changer qu'après évaluation d'un état
privilégié \(s_t\) par la barrière :

\[
\hat a_t=\pi(o_t),\qquad a_t=\operatorname{Gate}(s_t,o_t,\hat a_t).
\]

Si la décision est `Block`, aucune mutation n'a lieu. Le Planning Lab de
ShardJEPA implémente déjà cet ordre « observer, proposer, vérifier, agir ».
Cette séparation rejoint les architectures d'assurance à l'exécution étudiées
pour les composants apprenants [8].

Une barrière indépendante n'est toutefois pas automatiquement correcte. La
preuve de sûreté exige aussi un modèle de dangers, une visibilité suffisante de
l'état, un temps d'exécution borné, un repli vérifié et une validation dans le
domaine opérationnel prévu.

## 6. Correspondance avec ShardJEPA

ShardJEPA implémente actuellement :

- un micro-MLP déterministe à deux couches pour évaluer des états ;
- une mémoire exacte k-NN euclidienne pour petits jeux de données ;
- des prédicteurs latents et des raisonneurs Poincaré/Lorentz ;
- la quantification INT8/INT4 et l'accès mmap en lecture seule ;
- une planification bornée et des traces rejouables ;
- une barrière de sûreté privilégiée exécutée avant mutation ;
- des expériences déterministes d'observation partielle et de transport de
  messages fiable, retardé ou perdu.

### Prototypes nano-réseaux externes associés

Deux dépôts Hugging Face associés à l'auteur apportent des prototypes concrets,
mais externes à ShardJEPA :

| Dépôt | Artefacts vérifiables | Résultats rejoués pour cette publication |
|---|---|---|
| [CogniARC Nano-NN](https://huggingface.co/zedgamer/cogniarc-nano-nn) | classifieur de domaine 6→12→4, 136 paramètres ; prédicteur d'action 8→16→1, 161 paramètres ; entraînement NumPy et inférence Rust | action : 388/500, soit 77,6 % ; domaine : 3/4 exemples canoniques, mais 55/100 sur le lot synthétique publié au lieu des 75 % annoncés |
| [Botte Nano-NN](https://huggingface.co/zedgamer/botte-nano-nn) | six MLP JSON de 50 à 310 paramètres ; inférence Python/Rust | 10 tests unitaires Rust réussis ; aucune précision mesurable faute de données, de découpage et de script d'entraînement dans l'instantané audité |

Ces dépôts étayent la faisabilité d'un niveau de routage très compact et du
schéma « entraînement hors runtime → poids JSON → inférence Rust déterministe ».
Ils ne valident pas encore les gains système annoncés. Les latences de 5 µs et
les économies de 60 à 90 % de jetons restent à reproduire avec matériel,
compilateur, chauffe, répétitions, charge de routage et échantillons bruts. Le
détail est archivé dans
[`nano-nn-huggingface-audit.md`](../../artifacts/2026-07-29/nano-nn-huggingface-audit.md).

### Petits experts appris dans ShardJEPA

Le Pattern Lab autonome contient maintenant deux entraînements Rust réels. P0
est un vérificateur local de transition Soroban à 217 paramètres. Les graines
7, 17 et 29 atteignent 100 % sur 384 exemples de validation et 384 états
porteurs de 4 à 6 chiffres, tandis que les contrôles aux étiquettes mélangées
restent proches de 50 %. Comme toutes les longueurs sont projetées vers les
mêmes sept caractéristiques locales, ce résultat mesure une invariance locale,
pas l'apprentissage des retenues ou de l'arithmétique multicolonne.

P1 est un RNN Elman distinct à 961 paramètres, entraîné par rétropropagation
temporelle sur des traces multicolonnes explicites. L'entraînement s'arrête aux
propagations de longueur 3 ; le jeu OOD contient uniquement les longueurs 4 à 7.
Les trois graines atteignent 77,08–77,92 % en interpolation et 68,23–73,96 % en
OOD, contre 50 % pour la baseline sans propagation et 100 % pour l'oracle exact.
C'est un gain appris modeste et local à la tâche, pas un résultat de politique
de routage. L'oracle exact reste souverain. Les détails figurent dans
`TR-2026-002` et dans
[`current-validation.md`](../../artifacts/2026-08-01/current-validation.md).

Il n'implémente pas encore :

- de nano-réseau canonique intégré au runtime ;
- de plan LPAP/GEPA relié à de vrais capteurs ;
- d'ordonnanceur temps réel dur ;
- de routeur LLM local/cloud ;
- de backend d'actionneur physique ;
- de mesure énergétique sur matériel embarqué.

Les adaptateurs de capteurs, simulateurs, réseaux et actionneurs doivent rester
hors du runtime bas niveau `src/` et se connecter par des ports génériques.

## 7. Hypothèses falsifiables

- **H1 — Front de Pareto :** à réussite et sûreté comparables, le routage
  multi-cadence réduit énergie, p95 de latence, mémoire maximale ou appels cloud
  par rapport aux baselines toujours-LLM.
- **H2 — Respect des échéances :** les couches rapides respectent leur budget
  même si les couches langagières expirent ou perdent le réseau.
- **H3 — Dégradation sûre :** une proposition invalide ou un dépassement de
  ressources conduit à un blocage ou un repli borné sans mutation indue.
- **H4 — Valeur de la mémoire :** la récupération bornée améliore la reprise ou
  la réussite sur situations répétées sans croissance de latence inacceptable.

La thèse est affaiblie si le coût du routeur annule le gain, si la réussite se
dégrade à sûreté égale, si les erreurs des couches hautes traversent la barrière,
ou si une baseline plus simple domine le front de Pareto.

## 8. Protocole expérimental

Comparer sur les mêmes observations, actions et budgets :

1. contrôleur et planificateur déterministes sans LLM ;
2. petit LLM local appelé pour chaque tâche ;
3. LLM distant appelé pour chaque tâche lorsque le réseau est disponible ;
4. routeur multi-cadence proposé.

L'ablation du routage appris doit en plus comparer une règle transparente au
plus petit réseau compatible utilisant exactement le même schéma d'entrée. Les
poids et les découpages doivent être figés avant l'évaluation ; la calibration
et l'abstention doivent être publiées avec la précision.

Les scénarios doivent inclure plusieurs graines, du bruit capteur, des scènes
hors distribution, des messages retardés ou perdus, de la pression mémoire et
une connectivité intermittente. Les mesures minimales sont la réussite, les
violations de sûreté, les blocages, p50/p95/p99, les échéances manquées,
l'énergie par tâche réussie, le pic mémoire, la calibration, le taux d'appel au
cloud et le temps de reprise.

Toute affirmation « moins de 1 ms » ou « moins de 3 W » doit préciser matériel,
runtime, modèle, quantification, forme d'entrée, longueur de sortie, méthode de
chauffe et protocole statistique.

## 9. Feuille de route

### P0 — Fixture autonome

- ajouter des budgets de ressources et des déclarations de capacités au
  Planning Lab ;
- router entre règle, micro-NN, mémoire exacte et planificateur ;
- importer un nano-réseau audité derrière un adaptateur typé, rejouer ses tests
  d'inférence et de précision, et le maintenir non autoritaire ;
- conserver `SafetyGate` avant mutation ;
- ajouter bruit capteur, échéances, jetons d'énergie et connectivité aux traces ;
- comparer à un routage statique et à l'appel systématique du plus grand module.

### P1 — Adaptateur edge mesuré

- ajouter un adaptateur externe capteur/actionneur avec simulateur déterministe
  de repli ;
- mesurer temps, mémoire et énergie sur le matériel cible ;
- entraîner et calibrer le routeur sur des scénarios fixes, puis tester sur des
  graines et configurations inconnues ;
- borner admission et éviction de la mémoire épisodique.

### P2 — Délibération langagière

- intégrer un modèle local compact derrière un délai maximal et un contrat de
  proposition typé ;
- ajouter l'escalade distante avec politique de confidentialité et de réseau ;
- empêcher les deux niveaux langagiers de contourner la barrière de sûreté ;
- mesurer la distillation vers de plus petites politiques au lieu d'en supposer
  le bénéfice.

## 10. Limites et conclusion

Ce texte est une note de position et une spécification expérimentale, pas la
validation d'un agent mobile complet. Les expériences incarnées de ShardJEPA
restent déterministes, sans capteurs physiques, moteur, RTOS, routeur entraîné,
LLM embarqué ni mesure d'énergie. La décomposition proposée peut introduire de
nouvelles erreurs d'interface, des états périmés et une charge de vérification.
Les experts Soroban entraînés évaluent des traces synthétiques ; ils ne prouvent
ni la qualité du routage, ni le transfert inter-domaines, ni la réussite incarnée.
Les nano-réseaux Hugging Face restent des artefacts externes : leurs annonces de
latence et d'économie de jetons ne constituent pas une validation de ShardJEPA.
Les modèles vision-langage-action de bout en bout constituent une architecture
concurrente sérieuse.

La conclusion corrigée n'est donc pas « les LLM ne sont pas le futur ». Elle
est :

> L'agent incarné futur sera probablement hétérogène. Les modèles de langage
> pourront délibérer, mais des budgets explicites décideront quand les appeler,
> et une frontière locale assurée décidera ce qui peut réellement arriver dans
> le monde physique.

## Références

La bibliographie complète se trouve dans [`references.bib`](references.bib).
