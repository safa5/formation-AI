# Note de livraison REGSPEC-14151

| Date de livraison | Auteur | Traitement(s) concerné(s) |
|-------------------|--------|---------------------------|
| À compléter | À compléter | JOUINV |

## Problème

Dans la sortie PDF de JOUINV, les distributions et les distributions rappelées sont affichées dans le même bloc.
La part des distributions rappelables non encore rappelées n'est pas suivie.

## Correction apportée

Deux nouveaux blocs sont ajoutés à JOUINV : « Distributions de capital (rappelables/rappelées) » et « Distribution autres éléments (rappelables/rappelées) ».
Les montants rappelables et rappelés sont retirés des blocs existants et affichés dans ces nouveaux blocs.
Les blocs existants sont conservés : seul leur contenu change.
Pour les autres éléments, seules les raisons de distribution paramétrées sont prises en compte, et non toutes les raisons qui commencent par « R ».

## Fichiers livrés

| Fichier | Type | Modification |
|---------|------|--------------|
| À compléter | À compléter | À compléter |

## Paramétrage à faire

À compléter : le ticket indique que les raisons de distribution « autres éléments » à prendre en compte doivent être paramétrées, sans préciser le paramétrage.

## Tests à faire

- [ ] Lancer JOUINV en sortie PDF sur une part avec des distributions rappelables et rappelées, et vérifier qu'elles apparaissent dans le bloc « Distributions de capital (rappelables/rappelées) ». (proposé)
- [ ] Vérifier que ces mêmes montants n'apparaissent plus dans les blocs existants de distribution, et que ces blocs restent affichés. (proposé)
- [ ] Lancer JOUINV puis sa version modifiée avec les mêmes saisies en sorties TAB et FIC, et vérifier que les « autres montants distribués » des rappels de distribution (RDIS) sont identiques (retour REGSPEC-14291).

## Points d'attention

- Le retour REGSPEC-14291 (autres montants distribués des RDIS remis à zéro en TAB et FIC) est encore « To Do » dans Jira : à corriger ou à confirmer avant livraison.
- Ce retour cite une copie du traitement nommée JOUINVS : confirmer si c'est elle qui est livrée.
- La liste des fichiers modifiés n'est pas indiquée dans le ticket.
- La date de livraison prévue dans le ticket est le 06/11/2026 ; la date réelle reste à compléter.
- Retirés de la note : le nom du client, l'adresse de la VM de test, le portefeuille, les numéros de transactions et les montants cités dans le ticket.
