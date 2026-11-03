"""Contrôle QA de la synthèse des mouvements (specs/synthese-mouvements.md).

Calcule, à partir de data/mouvements_sample.csv, la synthèse attendue pour un
portefeuille et une période, et l'affiche au format de MVT_SYNTHESE.TXT :

    Code.portefeuille;Code.valeur;Type.mouvement;Nb.mouvements;Quantite;Montant
    <ptf>;<Code.valeur>;<Type.mouvement>;<nb>;<Σ quantité>;<Σ quantité × prix>
    <ptf>;TOTAL;;<nb total>;<Σ quantité>;<Σ montant>

Usage :
    python tests/controle_synthese.py <code_portefeuille> <date_debut> <date_fin> [--csv CHEMIN]

Contrôle des dates avant la synthèse (erreur, code retour 2) : format YYYYMMDD,
date valide, début <= fin, aucune date postérieure à la date du jour. Cette
dernière règle est propre au script : la spec ne la prévoit pas.

Limites (la spec ou le jeu de données ne permettent pas de les reproduire) :
- CA7 : le CSV ne contient pas Descriptif.portefeuille ; l'existence du
  portefeuille n'est pas vérifiable. Un code absent du CSV donne la sortie
  « aucun mouvement » avec un avertissement sur stderr, pas une anomalie.
- Arrondi du montant non fixé par la spec : ROUND_HALF_UP à 2 décimales
  (sans effet sur le jeu fourni).
- Format de Quantite non fixé par la spec : somme restituée telle quelle.
"""

import argparse
import csv
import sys
from datetime import datetime
from decimal import Decimal, ROUND_HALF_UP
from pathlib import Path

EN_TETE = "Code.portefeuille;Code.valeur;Type.mouvement;Nb.mouvements;Quantite;Montant"
CSV_DEFAUT = Path(__file__).resolve().parent.parent / "data" / "mouvements_sample.csv"
DEUX_DECIMALES = Decimal("0.01")


def date_yyyymmdd(valeur):
    if len(valeur) != 8 or not valeur.isdigit():
        raise argparse.ArgumentTypeError(f"date '{valeur}' : format YYYYMMDD attendu")
    try:
        datetime.strptime(valeur, "%Y%m%d")
    except ValueError:
        raise argparse.ArgumentTypeError(f"date '{valeur}' : date invalide")
    return valeur


def lire_mouvements(chemin):
    with open(chemin, newline="", encoding="utf-8") as fichier:
        return list(csv.DictReader(fichier, delimiter=";"))


def calculer_synthese(mouvements, portefeuille, debut, fin):
    """Retourne {(Code.valeur, Type.mouvement): [nb, quantité, montant]}."""
    synthese = {}
    for mvt in mouvements:
        if mvt["Code.portefeuille"] != portefeuille:
            continue
        # Bornes incluses (CA5) ; YYYYMMDD se compare comme une chaîne
        if not debut <= mvt["Date.effet"] <= fin:
            continue
        quantite = Decimal(mvt["Quantite.exercee"])
        montant = quantite * Decimal(mvt["Prix.entree.sortie"])
        cumul = synthese.setdefault((mvt["Code.valeur"], mvt["Type.mouvement"]),
                                    [0, Decimal(0), Decimal(0)])
        cumul[0] += 1
        cumul[1] += quantite
        cumul[2] += montant
    return synthese


def formater(portefeuille, synthese):
    def ligne(valeur, type_mvt, nb, quantite, montant):
        montant = montant.quantize(DEUX_DECIMALES, rounding=ROUND_HALF_UP)
        return f"{portefeuille};{valeur};{type_mvt};{nb};{quantite};{montant}"

    lignes = [EN_TETE]
    total = [0, Decimal(0), Decimal(0)]
    for (valeur, type_mvt), (nb, quantite, montant) in sorted(synthese.items()):
        lignes.append(ligne(valeur, type_mvt, nb, quantite, montant))
        total[0] += nb
        total[1] += quantite
        total[2] += montant
    lignes.append(ligne("TOTAL", "", *total))
    return lignes


def main():
    parser = argparse.ArgumentParser(description="Synthèse attendue des mouvements d'un portefeuille.")
    parser.add_argument("portefeuille", help="Code.portefeuille (ex. PTF001)")
    parser.add_argument("date_debut", type=date_yyyymmdd, help="YYYYMMDD, incluse")
    parser.add_argument("date_fin", type=date_yyyymmdd, help="YYYYMMDD, incluse")
    parser.add_argument("--csv", type=Path, default=CSV_DEFAUT, help="jeu de mouvements (défaut : %(default)s)")
    args = parser.parse_args()

    if args.date_debut > args.date_fin:
        parser.error("date_debut postérieure à date_fin")
    aujourd_hui = datetime.now().strftime("%Y%m%d")
    if args.date_fin > aujourd_hui:
        parser.error(f"période dans le futur (date du jour : {aujourd_hui})")

    mouvements = lire_mouvements(args.csv)
    if not any(mvt["Code.portefeuille"] == args.portefeuille for mvt in mouvements):
        print(f"AVERTISSEMENT : {args.portefeuille} absent du CSV ; existence dans "
              "Descriptif.portefeuille non vérifiable (CA7 non reproductible).", file=sys.stderr)

    synthese = calculer_synthese(mouvements, args.portefeuille, args.date_debut, args.date_fin)
    print("\n".join(formater(args.portefeuille, synthese)))


if __name__ == "__main__":
    main()
