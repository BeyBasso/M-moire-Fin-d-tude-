# CopilotBI Analyzer — Application Streamlit
## Thèse Professionnelle RNCP 37137 — Martine Bienvenue BASSOLE — OPmobility — 2025/2026

### Description
Application d'aide à la décision sur l'usage de Microsoft Copilot dans Power BI.
Intègre un modèle Random Forest (accuracy 96,7%) entraîné sur 200 observations terrain réelles.
Couvre 7 tâches Copilot Power BI : Analyser données, Générer DAX, Résumer insights,
Questions langage naturel, Créer rapports, Nettoyer données, Améliorer le design.

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

### Fichiers requis (même dossier)
- streamlit_app.py    → Application principale (8 pages)
- model_rf.pkl        → Modèle Random Forest entraîné
- metrics.json        → Métriques, paramètres et courbes ROC du modèle
- dataset_copilot.csv → Jeu de données (200 observations terrain réelles)
- requirements.txt    → Dépendances Python

### Pages de l'application
1. Tableau de bord     → Résultats de l'étude — gains par tâche
2. Recommandation IA   → Prédiction personnalisée + guide pratique
3. Comparateur         → 2 tâches côte à côte
4. Score de maturité   → Auto-évaluation UTAUT sur 5 axes
5. Performance modèle  → Matrice confusion, courbes ROC, importance variables
6. Tests statistiques  → t-test Welch, Cohen's d, IC 95%
7. Analyse ROI         → Coût-bénéfice, payback, projection 12 mois
8. Glossaire & À propos

### Compatibilité navigateur
Testé sous Chrome 120+, Firefox 125+, Edge 120+

### Conformité RGPD
Aucune donnée personnelle collectée. Données terrain anonymisées.
Classification AI Act : Système d'IA à faible risque (Art. 6).
Aucune connexion à un service externe lors des prédictions.

### Identifiants de test
Aucune authentification requise — accès direct.

### Contact
Auteure : Martine Bienvenue BASSOLE
Tuteur entreprise : Jean-Luc OBERLE
OPmobility — Direction des Achats, Business Group C-Power
Nexa Digital School — RNCP 37137