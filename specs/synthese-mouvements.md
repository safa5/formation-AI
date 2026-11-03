# Feature : Synthèse des mouvements d'un portefeuille sur une période

## Contexte métier

On veut un état de synthèse des mouvements d'un portefeuille sur une période, en texte brut, réutilisable par d'autres traitements. Là où `MVT.LISTE.MOUVEMENTS` liste chaque mouvement, la synthèse les agrège par valeur et par type de mouvement, avec un total pour le portefeuille.

La réutilisation passe par un fichier texte délimité `;` à format fixe, relu par les traitements consommateurs.

## Comportement attendu (Given / When / Then)

**Paramètres** : `Prm.code.portefeuille`, `Prm.date.debut`, `Prm.date.fin` (format `YYYYMMDD`).

**Format du fichier `MVT_SYNTHESE.TXT`** (pas de libellé libre, séparateur `;`) :

```
Code.portefeuille;Code.valeur;Type.mouvement;Nb.mouvements;Quantite;Montant
<ptf>;<Code.valeur>;<Type.mouvement>;<nb>;<Σ Quantite.exercee>;<Σ Quantite.exercee × Prix.entree.sortie>
...
<ptf>;TOTAL;;<nb total>;<Σ quantité>;<Σ montant>
```

**Scénario 1 — synthèse nominale**
- Given le portefeuille existe dans `Descriptif.portefeuille` et a des mouvements dont la `Date.effet` est dans la période
- When on lance le traitement avec ce portefeuille et cette période
- Then le fichier contient l'en-tête, puis une ligne par couple (`Code.valeur`, `Type.mouvement`), triée sur `Code.valeur` puis `Type.mouvement`, puis une ligne `TOTAL`

**Scénario 2 — bornes de période**
- Given des mouvements dont la `Date.effet` est égale à `Prm.date.debut` ou à `Prm.date.fin`
- When on lance le traitement
- Then ces mouvements sont pris en compte (bornes incluses) ; ceux hors période sont ignorés

**Scénario 3 — aucun mouvement sur la période**
- Given le portefeuille existe mais n'a aucun mouvement dans la période
- When on lance le traitement
- Then le fichier contient l'en-tête et la ligne `TOTAL` à 0 (`<ptf>;TOTAL;;0;0;0.00`)

**Scénario 4 — portefeuille inconnu**
- Given le code portefeuille n'existe pas dans `Descriptif.portefeuille`
- When on lance le traitement
- Then une anomalie `MISE.A.JOUR.ANOMALIE("ERR", "Portefeuille inconnu")` est levée et aucun fichier n'est écrit

## Contraintes techniques (stack, perfs, compat)

- ADL GP2016 ; nouvelle procédure `MVT.SYNTHESE.MOUVEMENTS (Prm.code.portefeuille, Prm.date.debut, Prm.date.fin)`.
- Fichier source en Windows-1252.
- Champs utilisés : uniquement ceux de `schema/extrait_schema.txt` (`Code.portefeuille`, `Code.valeur`, `Type.mouvement`, `Date.effet`, `Quantite.exercee`, `Prix.entree.sortie`) et des champs de travail locaux.
- Contrôle d'existence du portefeuille via `MVU.PORTEFEUILLE.EXISTE` (`BIBMVTUTIL.BIB`, non modifiée).
- Lecture : `FOR EACH Mouvement VIA (Code.portefeuille = ...)` avec clé seule dans `VIA` ; filtre période par `IF` dans le `DO` ; agrégation par rupture sur `SORTED ON Code.valeur, Type.mouvement`.
- Pas de filtre sur `Statut.ligne`.
- Montant au format décimal à 2 décimales, point comme séparateur.
- Traçabilité : `!IA/SAM 27/10/26` sur chaque bloc ajouté et dans la cartouche.

## Hors périmètre

- Filtre sur `Statut.ligne`.
- Montants en devise (`Prix.entree.sortie.dv`) ou conversion de devise.
- Plus-values (`Plus.value.long.terme.dc`, `Plus.value.court.terme.dc`).
- Plusieurs portefeuilles dans un même lancement.
- Modification de `MVT.LISTE.MOUVEMENTS` ou de `BIBMVTUTIL.BIB`.

## Critères d'acceptation (checklist testable)

- [ ] CA1 — La première ligne est exactement `Code.portefeuille;Code.valeur;Type.mouvement;Nb.mouvements;Quantite;Montant`.
- [ ] CA2 — Une ligne par couple (`Code.valeur`, `Type.mouvement`) présent sur la période, triée sur `Code.valeur` puis `Type.mouvement`.
- [ ] CA3 — `Nb.mouvements`, `Quantite` et `Montant` d'une ligne sont respectivement le nombre de mouvements, Σ `Quantite.exercee` et Σ (`Quantite.exercee` × `Prix.entree.sortie`) du couple.
- [ ] CA4 — La dernière ligne est `<ptf>;TOTAL;;<nb>;<qté>;<montant>`, égale à la somme des lignes de détail.
- [ ] CA5 — Les mouvements à `Date.effet` = date début ou date fin sont inclus ; ceux hors période sont exclus.
- [ ] CA6 — Sans mouvement sur la période : en-tête + `<ptf>;TOTAL;;0;0;0.00`.
- [ ] CA7 — Portefeuille inconnu : anomalie `Portefeuille inconnu`, aucun fichier écrit.
- [ ] CA8 — Jeu `data/mouvements_sample.csv`, `PTF001`, du `20260101` au `20260228` → fichier attendu :

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

## Fichiers concernés

- `adl/mag/mvt/mvt_synthese_mouvements.adl` — création
- `adl/bib/BIBMVTUTIL.BIB` — lecture seule (réutilisation de `MVU.PORTEFEUILLE.EXISTE`)
- `data/mouvements_sample.csv` — jeu de données du CA8
