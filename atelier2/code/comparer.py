
# comparer.py

import json
from pathlib import Path

DOSSIER = Path(__file__).resolve().parent.parent / "resultats"

resultats = []

# Load all evaluation result files
for fichier in sorted(DOSSIER.glob("*.json")):
    with open(fichier, encoding="utf-8") as f:
        resultats.append(json.load(f))

if not resultats:
    print("Aucun résultat trouvé.")
    print(f"Vérifiez le dossier : {DOSSIER}")
    raise SystemExit(0)

# Sort models by macro-F1, from highest to lowest
resultats.sort(key=lambda r: r["macro_f1"], reverse=True)

print("COMPARAISON DES MODÈLES")
print("-" * 82)

print(
    f"{'Modèle':<34}"
    f"{'Accuracy':>9}"
    f"{'Macro-F1':>10}"
    f"{'Invalides':>10}"
    f"{'Corrects':>9}"
    f"{'Durée (s)':>10}"
)

for r in resultats:
    corrects = round(r["accuracy"] * len(r["ids"]))

    print(
        f"{r['etiquette']:<34}"
        f"{r['accuracy']:>9.3f}"
        f"{r['macro_f1']:>10.3f}"
        f"{r['invalides']:>10.3f}"
        f"{corrects:>9}"
        f"{r['duree_s']:>10}"
    )

# Show tickets where models disagree
print("\nDÉSACCORDS ENTRE MODÈLES")

# Compare only if the result files use the same ticket order
reference = resultats[0]
ids = reference["ids"]
vrais = reference["vrais"]

for r in resultats[1:]:
    if r["ids"] != ids or r["vrais"] != vrais:
        print(
            "Attention : les résultats ne portent pas sur "
            "les mêmes tickets dans le même ordre."
        )
        raise SystemExit(1)

desaccords = 0

for i, id_ in enumerate(ids):
    avis = [r["predits"][i] for r in resultats]

    if len(set(avis)) > 1:
        desaccords += 1
        detail = " | ".join(
            f"{r['etiquette']} = {r['predits'][i]}"
            for r in resultats
        )

        print(f"{id_} (vrai : {vrais[i]}) : {detail}")

if desaccords == 0:
    print("Aucun désaccord entre les modèles.")

print(f"\nNombre de tickets avec désaccords : {desaccords}/{len(ids)}")
