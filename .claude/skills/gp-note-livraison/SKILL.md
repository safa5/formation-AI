---
name: gp-note-livraison
description: Rédige la note de livraison d'une correction GP (programme ADL, BIB, paramétrage), toujours au même format, à partir des informations données par le développeur. À utiliser quand on demande « fais la note de livraison », « prépare la livraison du ticket PRJ-1234 », « rédige la release note » ou « note de livraison du ticket X ».
argument-hint: "<ticket> <informations ou fichier>"
---

# Note de livraison GP

Demande : $ARGUMENTS

## Méthode

1. Relever dans la demande, ou dans le fichier indiqué :
   - le numéro de ticket ;
   - le ou les traitements GP concernés (code de 6 lettres, ex. VALOPC) ;
   - les fichiers modifiés ;
   - la description du problème ;
   - la description de la correction ;
   - le paramétrage à faire ;
   - les tests à faire.
   Sans numéro de ticket : le demander et ne rien rédiger avant de l'avoir.
2. Lire le modèle `templates/note-livraison.md` et le remplir rubrique par rubrique :
   - Type de fichier : `adl` pour un .adl, `bib` pour un .bib, `paramétrage` pour un paramétrage.
   - Paramétrage à faire : « Aucun » si la demande dit qu'il n'y en a pas, « À compléter » si elle n'en parle pas.
   - Tests à faire : si aucun test n'est donné, proposer 1 à 3 tests déduits de la correction, chacun suivi de « (proposé) ».
3. Contrôler la note avec la liste de contrôle ci-dessous et la corriger avant de la rendre.
4. Enregistrer la note dans `livraisons/<ticket>-note-livraison.md` et donner le chemin.

## Règles

- N'invente rien : une information absente s'écrit « À compléter », y compris l'auteur et la date de livraison.
- Dates au format JJ/MM/AAAA.
- Codes traitement en majuscules.
- Une phrase par idée, sans jargon inutile : la note est lue aussi par le support.
- Jamais de donnée client, de mot de passe ni de valeur de production dans la note. Si la demande en contient, ne pas les recopier et signaler leur retrait dans « Points d'attention ».

## Liste de contrôle

- [ ] Toutes les rubriques du modèle sont présentes, dans l'ordre.
- [ ] Chaque fichier cité dans la demande est dans le tableau.
- [ ] Chaque information manquante est marquée « À compléter ».
