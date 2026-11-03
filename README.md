# gp-tp-specdriven — projet support du TP « Spec-Driven Development sur GP »

Mini-projet **volontairement partiel** : il ne contient que ce qui est nécessaire au TP. Ce n'est pas un module GP livrable.

## Contenu

```
gp-tp-specdriven/
├── CLAUDE.md                          Contexte et règles lus automatiquement par Claude Code
├── README.md                          Ce fichier
├── adl/
│   ├── mag/mvt/mvt_liste_mouvements.adl   Procédure existante : liste des mouvements d'un portefeuille sur une période
│   └── bib/BIBMVTUTIL.BIB                 Bibliothèque utilitaire (préfixe MVU)
├── schema/extrait_schema.txt          Extrait des relations Mouvement et Descriptif.portefeuille (GP2016)
├── data/mouvements_sample.csv         Jeu de données d'exemple (2 portefeuilles, codes fictifs)
├── specs/_gabarit.md                  Gabarit de spec à respecter
├── tests/                             Zone QA (cas de test, script de contrôle)
└── livrables/mesures.md               Tableau de mesures à remplir pendant le TP
```

## Points d'attention

- Les fichiers `.adl` / `.bib` sont encodés en **Windows-1252**, comme dans le dépôt GP.
- Le code ADL fourni n'a pas été compilé : c'est un support de lecture et de génération, pas un module à livrer.
- Pas de Git dans ce TP : les points de départ propres s'obtiennent en **dézippant à nouveau** l'archive dans un autre dossier.
