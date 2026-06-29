# CopilotBI Analyzer — Application Streamlit
## Thèse Professionnelle RNCP 37137 — Martine Bienvenue BASSOLE — OPmobility — 2025/2026

### Description
Application d'aide à la décision sur l'usage de Microsoft Copilot dans Power BI.
Intègre un modèle Random Forest (accuracy 89,9%, CV 0,901, AUC 0,961) entraîné sur
plus de 10 500 observations issues des données OPmobility stockées sur Databricks.
Couvre 7 tâches Copilot Power BI : Analyser les données rapidement, Générer du DAX,
Résumer les insights, Poser des questions en langage naturel, Créer des rapports
automatiquement, Nettoyer les données, Améliorer le design.

> Données confidentielles OPmobility — non publiables. Voir politique de confidentialité
> du groupe pour toute question relative à l'accès aux données sources.

### Application en ligne
https://9495qvbkuadec7ruindcux.streamlit.app

### Prérequis
- Python 3.10+
- pip

### Installation
pip install -r requirements.txt

### Lancement
streamlit run streamlit_app.py
Accéder à : http://localhost:8501

### Fichiers requis (même dossier que streamlit_app.py)
- streamlit_app.py    → Application principale (8 pages)
- model_rf.pkl        → Modèle Random Forest entraîné (200 arbres, profondeur max 10)
- metrics.json        → Métriques, gains de référence, temps de référence, courbes ROC
- dataset_copilot.csv → Jeu de données OPmobility/Databricks (10 500+ observations)
- requirements.txt    → Dépendances Python

> Important : les quatre fichiers de données doivent se trouver dans le même dossier
> que streamlit_app.py. Le script utilise des chemins absolus basés sur __file__ pour
> éviter les erreurs de chemin selon le répertoire de lancement.

### Pages de l'application
1. Tableau de bord      → Résultats de l'étude — gains par tâche, impact niveau d'expertise
2. Recommandation IA    → Prédiction Random Forest personnalisée + guide pratique opérationnel
3. Score de maturité    → Auto-évaluation UTAUT sur 5 axes, radar personnalisé
4. Performance modèle   → Matrice de confusion, courbes ROC, importance variables Gini
5. Tests statistiques   → t-test de Welch, Cohen's d, intervalles de confiance 95%
6. Analyse ROI          → Coût-bénéfice, seuil de rentabilité, projection 12 mois
7. Glossaire            → Copilot & Power BI, DAX & modélisation, machine learning
8. À propos             → Contexte, architecture Databricks, conformité RGPD et AI Act

### Variables du modèle
Le modèle Random Forest utilise 10 variables d'entrée :
- type_tache       → Type de tâche Copilot parmi les 7 catégories
- complexite       → Niveau de complexité (Faible / Moyen / Élevé)
- type_livrable    → Destinataire du livrable (Opérationnel / Pilotage / Exploratoire)
- niveau_expertise → Niveau Power BI de l'utilisateur (Débutant / Intermédiaire / Expert)
- temps_realisation_min, nb_iterations, score_pertinence, score_clarte,
  score_exactitude, score_exploitabilite

Variable cible : copilot_pertinent (binaire) — 1 si gain > 10%, score moyen >= 3,5/5
et nb corrections <= 3, simultanément.

### Performances du modèle
- Accuracy        : 89,9%
- Validation croisée (5 plis) : 0,901 ± 0,004
- AUC ROC         : 0,961
- Hyperparamètres : 200 arbres, profondeur max 10, min_samples_split 2, critère Gini

### Compatibilité navigateur
Testé sous Chrome 120+, Firefox 125+, Edge 120+

### Conformité RGPD
Aucune donnée personnelle collectée ou traitée par l'application.
Les données du dataset sont des données d'entreprise anonymisées.
Aucune connexion à un service externe lors des prédictions.
Classification AI Act : Système d'IA à risque minimal (Art. 6 du Règlement UE 2024/1689).

### Accès
Aucune authentification requise — accès direct depuis n'importe quel navigateur.

### Contact
Auteure : Martine Bienvenue BASSOLE
Tuteur entreprise : Jean-Luc OBERLE
OPmobility — Direction des Achats, Business Group C-Power
Nexa Digital School — RNCP 37137 Chef de projet Data & IA