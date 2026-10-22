# evaluer.py

import csv
import json
import re
import sys
import time
from pathlib import Path

from classifieur import CONSIGNE, classer
from evaluation import afficher_rapport


PAUSE = 2.1  # Respect the API rate limit
DOSSIER_ATELIER = Path(__file__).resolve().parent.parent
DOSSIER_RESULTATS = DOSSIER_ATELIER / "resultats"
FICHIER_CSV = DOSSIER_ATELIER / "data" / "tickets.csv"


def charger(chemin=FICHIER_CSV):
    """Charge les tickets depuis le fichier CSV."""
    with open(chemin, encoding="utf-8", newline="") as f:
        return list(csv.DictReader(f))


def evaluer(modele, lignes, consigne=CONSIGNE, etiquette=None):
    """Évalue un modèle et enregistre les résultats au format JSON."""
    if not lignes:
        raise ValueError("Le fichier CSV ne contient aucun ticket.")

    etiquette = etiquette or modele
    vrais = []
    predits = []
    debut = time.time()

    for i, ligne in enumerate(lignes):
        prediction = classer(
            ligne["texte"],
            modele,
            consigne=consigne,
        )

        predits.append(prediction)
        vrais.append(ligne["categorie"])

        # Avoid waiting after the final request
        if i < len(lignes) - 1:
            time.sleep(PAUSE)

    resume = afficher_rapport(etiquette, vrais, predits)

    resume.update(
        modele=modele,
        etiquette=etiquette,
        duree_s=round(time.time() - debut, 1),
        predits=predits,
        vrais=vrais,
        ids=[ligne["id"] for ligne in lignes],
    )

    # Save results to resultats/<label>.json
    nom = re.sub(r"[^A-Za-z0-9._-]+", "_", etiquette)
    fichier_sortie = DOSSIER_RESULTATS / f"{nom}.json"

    DOSSIER_RESULTATS.mkdir(parents=True, exist_ok=True)

    with open(fichier_sortie, "w", encoding="utf-8") as f:
        json.dump(resume, f, ensure_ascii=False, indent=2)

    print(f"\nRésultats enregistrés dans : {fichier_sortie}")

    return resume


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print(
            "Usage : python evaluer.py NOM_DU_MODELE",
            file=sys.stderr,
        )
        sys.exit(1)

    modele = sys.argv[1]
    lignes = charger()
    evaluer(modele, lignes)
