
# evaluation.py

CATEGORIES = ["facturation", "technique", "compte", "commercial"]


def accuracy(vrais, predits):
    if not vrais:
        return 0.0

    return sum(
        1 for v, p in zip(vrais, predits) if v == p
    ) / len(vrais)


def scores_par_classe(vrais, predits, classes=CATEGORIES):
    resultat = {}

    for c in classes:
        vp = sum(
            1 for v, p in zip(vrais, predits)
            if v == c and p == c
        )
        fp = sum(
            1 for v, p in zip(vrais, predits)
            if v != c and p == c
        )
        fn = sum(
            1 for v, p in zip(vrais, predits)
            if v == c and p != c
        )

        precision = vp / (vp + fp) if (vp + fp) else 0.0
        recall = vp / (vp + fn) if (vp + fn) else 0.0

        f1 = (
            2 * precision * recall / (precision + recall)
            if (precision + recall)
            else 0.0
        )

        resultat[c] = {
            "precision": precision,
            "recall": recall,
            "f1": f1,
            "support": vp + fn,
        }

    return resultat


def f1_macro(scores):
    if not scores:
        return 0.0

    return sum(d["f1"] for d in scores.values()) / len(scores)


def taux_invalides(predits):
    if not predits:
        return 0.0

    return sum(1 for p in predits if p == "invalide") / len(predits)


def matrice_confusion(vrais, predits, classes=CATEGORIES):
    # Rows = true category, columns = predicted category (+ "invalide")
    colonnes = list(classes) + ["invalide"]

    matrice = {
        v: {c: 0 for c in colonnes}
        for v in classes
    }

    for v, p in zip(vrais, predits):
        if v in matrice and p in matrice[v]:
            matrice[v][p] += 1

    return matrice


def afficher_rapport(etiquette, vrais, predits):
    if len(vrais) != len(predits):
        raise ValueError(
            "Le nombre de vérités doit être égal au nombre de prédictions."
        )

    scores = scores_par_classe(vrais, predits)
    acc = accuracy(vrais, predits)
    macro = f1_macro(scores)
    inval = taux_invalides(predits)
    matrice = matrice_confusion(vrais, predits)

    print(f"\n=== {etiquette} ===")
    print(f"Accuracy : {acc:.3f}")
    print(f"Macro-F1 : {macro:.3f}")
    print(f"Taux d'invalides : {inval:.3f}")

    print(
        f"\n{'categorie':<13}"
        f"{'precision':>10}"
        f"{'recall':>8}"
        f"{'F1':>8}"
        f"{'n':>5}"
    )

    for c, d in scores.items():
        print(
            f"{c:<13}"
            f"{d['precision']:>10.3f}"
            f"{d['recall']:>8.3f}"
            f"{d['f1']:>8.3f}"
            f"{d['support']:>5}"
        )

    colonnes = list(CATEGORIES) + ["invalide"]

    print("\nMatrice de confusion")
    print("(lignes = vérité, colonnes = prédiction)")
    print(" " * 13 + "".join(f"{c[:6]:>8}" for c in colonnes))

    for v in CATEGORIES:
        print(
            f"{v:<13}"
            + "".join(f"{matrice[v][c]:>8}" for c in colonnes)
        )

    return {
        "accuracy": acc,
        "macro_f1": macro,
        "invalides": inval,
        "par_classe": scores,
        "matrice": matrice,
    }
