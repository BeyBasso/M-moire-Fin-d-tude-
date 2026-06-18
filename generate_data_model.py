import pandas as pd
import numpy as np
import json
import pickle
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split, GridSearchCV, cross_val_score
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics import accuracy_score, confusion_matrix, classification_report

np.random.seed(42)

TACHES = [
    "Créer des rapports automatiquement",
    "Analyser les données rapidement",
    "Poser des questions en langage naturel",
    "Générer du DAX",
    "Nettoyer les données",
    "Améliorer le design",
    "Résumer les insights",
]

COMPLEXITES = ["Faible", "Moyen", "Élevé"]
LIVRABLES   = ["Opérationnel", "Management", "Exploratoire"]

# Profils par tâche : (gain_pct, qual_base, iter_base, copilot_proba)
PROFILS = {
    "Créer des rapports automatiquement":    (0.35, 4.0, 2, 0.85),
    "Analyser les données rapidement":        (0.40, 4.2, 2, 0.85),
    "Poser des questions en langage naturel": (0.45, 4.3, 1, 0.90),
    "Générer du DAX":                         (0.08, 3.4, 4, 0.25),
    "Nettoyer les données":                   (0.20, 3.8, 3, 0.60),
    "Améliorer le design":                    (0.30, 4.0, 2, 0.75),
    "Résumer les insights":                   (0.45, 4.3, 1, 0.90),
}

rows = []
for _ in range(120):
    task  = np.random.choice(TACHES)
    compl = np.random.choice(COMPLEXITES)
    deliv = np.random.choice(LIVRABLES)
    gain_pct, qual_base, iter_base, cop_proba = PROFILS[task]

    # Ajustements complexité
    compl_mult = {"Faible": 0.8, "Moyen": 1.0, "Élevé": 1.3}[compl]
    iter_add   = {"Faible": -1, "Moyen": 0, "Élevé": 1}[compl]

    temps_sans = int(np.random.normal(45 * compl_mult, 8))
    temps_sans = max(10, temps_sans)

    copilot_utilise = int(np.random.random() < cop_proba)
    temps_avec = int(temps_sans * (1 - gain_pct)) if copilot_utilise else temps_sans

    nb_iter = max(1, iter_base + iter_add + int(np.random.normal(0, 0.5)))
    qual = min(5.0, max(1.0, round(np.random.normal(
        qual_base if copilot_utilise else qual_base - 0.3, 0.3), 1)))

    rows.append({
        "type_tache":            task,
        "complexite":            compl,
        "type_livrable":         deliv,
        "temps_realisation_min": temps_avec if copilot_utilise else temps_sans,
        "nb_iterations":         nb_iter,
        "score_pertinence":      qual,
        "score_clarte":          round(qual + np.random.normal(0, 0.2), 1),
        "score_exactitude":      round(qual + np.random.normal(0, 0.2), 1),
        "score_exploitabilite":  round(qual + np.random.normal(0, 0.2), 1),
        "copilot_utilise":       copilot_utilise,
    })

df = pd.DataFrame(rows)
df["score_clarte"]       = df["score_clarte"].clip(1, 5)
df["score_exactitude"]   = df["score_exactitude"].clip(1, 5)
df["score_exploitabilite"] = df["score_exploitabilite"].clip(1, 5)

df.to_csv("/home/claude/dataset_copilot.csv", index=False)
print(f"Dataset généré : {len(df)} lignes")
print(df["type_tache"].value_counts())
print(f"Copilot utilisé : {df['copilot_utilise'].sum()}/{len(df)}")

# ── Entraînement ─────────────────────────────────────────
le_task  = LabelEncoder().fit(df["type_tache"])
le_compl = LabelEncoder().fit(df["complexite"])
le_deliv = LabelEncoder().fit(df["type_livrable"])

df["task_enc"]  = le_task.transform(df["type_tache"])
df["compl_enc"] = le_compl.transform(df["complexite"])
df["deliv_enc"] = le_deliv.transform(df["type_livrable"])

FEATURES = ["task_enc","compl_enc","deliv_enc","temps_realisation_min","nb_iterations",
            "score_pertinence","score_clarte","score_exactitude","score_exploitabilite"]

X = df[FEATURES]
y = df["copilot_utilise"]

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.25, random_state=42, stratify=y)

param_grid = {
    "n_estimators":    [100, 200],
    "max_depth":       [4, 6, None],
    "min_samples_split": [2, 5],
}
rf = GridSearchCV(RandomForestClassifier(random_state=42), param_grid, cv=5, scoring="accuracy", n_jobs=-1)
rf.fit(X_train, y_train)

best = rf.best_estimator_
y_pred = best.predict(X_test)
acc = accuracy_score(y_test, y_pred)
cv_scores = cross_val_score(best, X, y, cv=5, scoring="accuracy")
cm = confusion_matrix(y_test, y_pred)
fi = dict(zip(FEATURES, best.feature_importances_.tolist()))

print(f"\nAccuracy : {acc:.3f}")
print(f"CV scores : {cv_scores}")
print(f"Best params : {rf.best_params_}")
print(f"\nClassification report:\n{classification_report(y_test, y_pred)}")

metrics = {
    "accuracy":          acc,
    "cv_scores":         cv_scores.tolist(),
    "confusion_matrix":  cm.tolist(),
    "feature_importances": fi,
    "best_params":       rf.best_params_,
    "train_size":        len(X_train),
    "test_size":         len(X_test),
}
with open("/home/claude/metrics.json", "w") as f:
    json.dump(metrics, f, indent=2)

bundle = {"model": best, "le_task": le_task, "le_compl": le_compl,
          "le_deliv": le_deliv, "features": FEATURES}
with open("/home/claude/model_rf.pkl", "wb") as f:
    pickle.dump(bundle, f)

print("\n✅ model_rf.pkl, metrics.json et dataset_copilot.csv générés avec succès.")
