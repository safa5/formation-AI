# CLAUDE.md — gp-tp-specdriven

## Contexte

Projet support d'un TP sur la solution GP (MAGNUM GP2016) de NeoXam. Le langage est l'**ADL**, langage procédural natif de MAGNUM.

- Procédures : `adl/mag/` — Bibliothèques : `adl/bib/`
- Schéma de référence (extrait) : `schema/extrait_schema.txt`
- Données d'exemple : `data/mouvements_sample.csv`
- Specs : `specs/` — Tests QA : `tests/` — Livrables du TP : `livrables/`

## Règles de travail

- N'utilise **que** les champs présents dans `schema/extrait_schema.txt` ou déjà déclarés dans le code. Si un champ manque, **pose la question** au lieu d'en inventer un.
- Quand une spec est fournie : implémente **uniquement** ce qu'elle contient. Si un point est ambigu, pose la question.
- Ne modifie pas `adl/bib/BIBMVTUTIL.BIB` sauf si la spec le demande explicitement.
- Pas de Git dans ce projet.

## Règles ADL (non négociables)

- Encodage **Windows-1252** pour `.adl` / `.bib` : ne jamais réécrire ces fichiers en UTF-8.
- `FIELD` déclarés en zone FIELD, avant tout traitement ; jamais dans une `MACRO` / `FUNCTION` ; jamais de champ déclaré non utilisé ni redéclaré.
- `MACRO` : fermée par `END.MACRO`, jamais de `RETURNING`.
- Fonction booléenne (`SAME AS Booleen`) : initialiser à `Mag.false`, passer à `Mag.true` si la condition est vérifiée.
- `SELECT` / `FOR EACH` : dans `VIA`, uniquement le nom du champ clé ; filtrer les champs DATA par `IF` dans le `THEN` / `DO`.
- `ALTER` n'accepte jamais de `VIA` : `SELECT ... VIA (...)` puis `ALTER ... USING (...)`.
- Champs locaux d'une BIB préfixés (ici `MVU.`).
- Commentaires au format `!` (pas de mélange avec `% ... %` hors cartouche).
- Erreurs : `MISE.A.JOUR.ANOMALIE`.
- Traçabilité : tout bloc ajouté ou modifié porte `!IA/<trigramme> <JJ/MM/AA> <jira_id>` (sans jira_id si aucun ticket).
