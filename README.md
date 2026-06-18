# CopilotBI Analyzer — Application Streamlit
## Thèse Professionnelle RNCP 37137 — Martine Bassolé — OPmobility — 2025/2026

### Description
Application d'aide à la décision sur l'usage de Copilot dans Power BI.
Intègre un modèle Random Forest (accuracy 96,7%) entraîné sur 120 observations terrain.

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
- streamlit_app.py    → Application principale
- model_rf.pkl        → Modèle Random Forest entraîné
- metrics.json        → Métriques et paramètres du modèle
- dataset_copilot.csv → Jeu de données (120 obs., anonymisé)
- requirements.txt    → Dépendances Python

### Compatibilité navigateur
Testé sous Chrome 120+, Firefox 125+, Edge 120+

### Conformité RGPD
Aucune donnée personnelle collectée. Données anonymisées.
Classification AI Act : Système d'IA à faible risque (Art. 6).

### Identifiants de test
Aucune authentification requise — accès direct.

### Contact
Auteure : Martine Bassolé | OPmobility — Direction des Achats, 
Business Group C-Power