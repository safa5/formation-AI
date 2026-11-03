# Cas de test — Synthèse des mouvements d'un portefeuille

- **Spec** : `specs/synthese-mouvements.md`
- **Procédure testée** : `MVT.SYNTHESE.MOUVEMENTS (Prm.code.portefeuille, Prm.date.debut, Prm.date.fin)`
- **Fichier produit** : `MVT_SYNTHESE.TXT`
- **Données** : `data/mouvements_sample.csv`
- **Référence calculée** : `python tests/controle_synthese.py <ptf> <debut> <fin>`

## Préconditions communes

- P1 — Les mouvements de `data/mouvements_sample.csv` sont chargés dans `Mouvement` (mode de chargement : voir point 2).
- P2 — `PTF001` existe dans `Descriptif.portefeuille`.
- P3 — `MVT_SYNTHESE.TXT` est absent avant chaque lancement.

## Lignes du jeu utilisées (PTF001)

| Date.effet | Code.valeur | Type.mouvement | Quantite.exercee | Prix.entree.sortie | Quantité × prix |
|---|---|---|---|---|---|
| 20260102 | FR0000120271 | ACH | 1000 | 54.20 | 54200.00 |
| 20260105 | FR0000131104 | ACH | 500 | 61.75 | 30875.00 |
| 20260112 | FR0000120271 | VEN | 300 | 55.10 | 16530.00 |
| 20260120 | US0378331005 | ACH | 200 | 185.40 | 37080.00 |
| 20260203 | FR0000131104 | VEN | 500 | 63.00 | 31500.00 |
| 20260210 | FR0000120578 | ACH | 750 | 92.30 | 69225.00 |
| 20260228 | US0378331005 | VEN | 50 | 190.15 | 9507.50 |

---

## CT1 — CA1 : en-tête

- **Préconditions** : P1, P2, P3.
- **Données** : les 7 mouvements PTF001 ci-dessus.
- **Étapes** :
  1. Lancer `MVT.SYNTHESE.MOUVEMENTS ("PTF001", "20260101", "20260228")`.
  2. Lire la première ligne de `MVT_SYNTHESE.TXT`.
- **Résultat attendu** : la ligne 1 est exactement `Code.portefeuille;Code.valeur;Type.mouvement;Nb.mouvements;Quantite;Montant`.
- **Testabilité** : OK.

## CT2 — CA2 : une ligne par couple, triée

- **Préconditions** : P1, P2, P3.
- **Données** : les 7 mouvements PTF001 ci-dessus.
- **Étapes** :
  1. Lancer `MVT.SYNTHESE.MOUVEMENTS ("PTF001", "20260101", "20260228")`.
  2. Relever les lignes entre l'en-tête et la ligne `TOTAL`.
- **Résultat attendu** : 7 lignes de détail, une par couple, dans cet ordre :
  `FR0000120271;ACH`, `FR0000120271;VEN`, `FR0000120578;ACH`, `FR0000131104;ACH`, `FR0000131104;VEN`, `US0378331005;ACH`, `US0378331005;VEN`.
- **Testabilité** : **partiel**. Dans le CSV, aucun couple (`Code.valeur`, `Type.mouvement`) n'a plus d'un mouvement. Le regroupement de plusieurs mouvements en une seule ligne n'est donc pas exercé (point 5).

## CT3 — CA3 : Nb, Quantite, Montant par couple

- **Préconditions** : P1, P2, P3.
- **Données** : les 7 mouvements PTF001 ci-dessus.
- **Étapes** :
  1. Lancer `MVT.SYNTHESE.MOUVEMENTS ("PTF001", "20260101", "20260228")`.
  2. Comparer chaque ligne de détail au tableau du jeu.
- **Résultat attendu** : pour chaque couple, `Nb.mouvements` = 1, `Quantite` = `Quantite.exercee` et `Montant` = colonne « Quantité × prix » du tableau. Par exemple `PTF001;FR0000120271;ACH;1;1000;54200.00` et `PTF001;US0378331005;VEN;1;50;9507.50`.
- **Testabilité** : **partiel**. Les sommes sur plusieurs mouvements et un `Nb.mouvements` > 1 ne sont pas exercés : aucun couple ne se répète dans le CSV, tous portefeuilles confondus (point 5).

## CT4 — CA4 : ligne TOTAL

- **Préconditions** : P1, P2, P3.
- **Données** : les 7 mouvements PTF001 ci-dessus.
- **Étapes** :
  1. Lancer `MVT.SYNTHESE.MOUVEMENTS ("PTF001", "20260101", "20260228")`.
  2. Lire la dernière ligne et la comparer à la somme des lignes de détail.
- **Résultat attendu** : la dernière ligne est `PTF001;TOTAL;;7;3300;248917.50`. 7 = nombre de mouvements, 3300 = Σ quantités, 248917.50 = Σ montants. `Type.mouvement` est vide.
- **Testabilité** : OK.

## CT5 — CA5 : bornes de période incluses

- **Préconditions** : P1, P2, P3.
- **Données** : les 7 mouvements PTF001. Période choisie pour que des mouvements tombent sur chaque borne et en dehors :
  - borne début 20260105 : mouvement FR0000131104 ACH ;
  - borne fin 20260210 : mouvement FR0000120578 ACH ;
  - hors période : 20260102 et 20260228.
- **Étapes** :
  1. Lancer `MVT.SYNTHESE.MOUVEMENTS ("PTF001", "20260105", "20260210")`.
  2. Comparer le fichier au résultat attendu.
- **Résultat attendu** :
  ```
  Code.portefeuille;Code.valeur;Type.mouvement;Nb.mouvements;Quantite;Montant
  PTF001;FR0000120271;VEN;1;300;16530.00
  PTF001;FR0000120578;ACH;1;750;69225.00
  PTF001;FR0000131104;ACH;1;500;30875.00
  PTF001;FR0000131104;VEN;1;500;31500.00
  PTF001;US0378331005;ACH;1;200;37080.00
  PTF001;TOTAL;;5;2250;185210.00
  ```
  Les lignes `FR0000120271;ACH` (20260102) et `US0378331005;VEN` (20260228) sont absentes.
- **Testabilité** : OK.

## CT6 — CA6 : aucun mouvement sur la période

- **Préconditions** : P1, P2, P3.
- **Données** : PTF001 n'a aucun mouvement entre 20260301 et 20260331.
- **Étapes** :
  1. Lancer `MVT.SYNTHESE.MOUVEMENTS ("PTF001", "20260301", "20260331")`.
  2. Lire le fichier.
- **Résultat attendu** : exactement 2 lignes :
  ```
  Code.portefeuille;Code.valeur;Type.mouvement;Nb.mouvements;Quantite;Montant
  PTF001;TOTAL;;0;0;0.00
  ```
- **Testabilité** : OK.

## CT7 — CA7 : portefeuille inconnu

- **Préconditions** : P1, P3. `PTF999` n'existe pas dans `Descriptif.portefeuille` (point 3).
- **Données** : code `PTF999`, absent du CSV.
- **Étapes** :
  1. Lancer `MVT.SYNTHESE.MOUVEMENTS ("PTF999", "20260101", "20260228")`.
  2. Relever l'anomalie levée.
  3. Vérifier l'absence de `MVT_SYNTHESE.TXT`.
- **Résultat attendu** : l'anomalie `MISE.A.JOUR.ANOMALIE("ERR", "Portefeuille inconnu")` est levée et aucun fichier `MVT_SYNTHESE.TXT` n'est écrit.
- **Testabilité** : **conditionnel**, selon les points 1, 3 et 4. Non reproductible par `controle_synthese.py`, car le CSV ne porte pas `Descriptif.portefeuille`.

## CT8 — CA8 : jeu complet PTF001, janvier–février 2026

- **Préconditions** : P1, P2, P3.
- **Données** : `data/mouvements_sample.csv`, `PTF001`, du `20260101` au `20260228`.
- **Étapes** :
  1. Lancer `MVT.SYNTHESE.MOUVEMENTS ("PTF001", "20260101", "20260228")`.
  2. Comparer le fichier caractère pour caractère au bloc ci-dessous.
- **Résultat attendu** :
  ```
  Code.portefeuille;Code.valeur;Type.mouvement;Nb.mouvements;Quantite;Montant
  PTF001;FR0000120271;ACH;1;1000;54200.00
  PTF001;FR0000120271;VEN;1;300;16530.00
  PTF001;FR0000120578;ACH;1;750;69225.00
  PTF001;FR0000131104;ACH;1;500;30875.00
  PTF001;FR0000131104;VEN;1;500;31500.00
  PTF001;US0378331005;ACH;1;200;37080.00
  PTF001;US0378331005;VEN;1;50;9507.50
  PTF001;TOTAL;;7;3300;248917.50
  ```
- **Testabilité** : OK.

---

## Points non testables / à clarifier

1. **Emplacement de `MVT_SYNTHESE.TXT`** : non précisé par la spec. Il faut le connaître pour lire le fichier (CT1 à CT8) et pour constater son absence (CT7).
2. **Chargement du CSV dans `Mouvement`** : mode non précisé. La colonne `Devise.portefeuille` du CSV n'est pas utilisée (devise hors périmètre).
3. **`Descriptif.portefeuille`** : la présence de PTF001 et l'absence de PTF999 ne sont pas portées par le CSV. L'environnement de test doit les garantir.
4. **Observation de l'anomalie** : la spec ne dit pas où l'anomalie levée par `MISE.A.JOUR.ANOMALIE` est visible (log, écran ou table).
5. **Agrégation (CA2, CA3)** : il faut un jeu où au moins un couple (`Code.valeur`, `Type.mouvement`) a plusieurs mouvements sur la période. À fournir, ou à acter comme non testé.
6. **Arrondi et format de `Quantite`** : la règle d'arrondi du montant et le format de `Quantite` ne sont pas fixés par la spec. Le jeu fourni ne produit ni arrondi ni quantité décimale.
