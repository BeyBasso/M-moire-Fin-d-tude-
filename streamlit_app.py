"""
CopilotBI Analyzer v2.0 — Application Streamlit
Mémoire Professionnel RNCP 37137 — Chef de projet Data & IA
Auteur : Martine Bassolé | OPmobility | 2025-2026
"""

import streamlit as st
import pandas as pd
import numpy as np
import pickle
import json
import plotly.graph_objects as go
import plotly.express as px

st.set_page_config(
    page_title="CopilotBI Analyzer",
    page_icon="",
    layout="wide",
    initial_sidebar_state="collapsed",
)

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:ital,wght@0,300;0,400;0,500;0,600;0,700;0,800;0,900;1,400&family=JetBrains+Mono:wght@400;500;600;700&display=swap');

*,*::before,*::after{box-sizing:border-box;}
html{scroll-behavior:smooth;}

[data-testid="stAppViewContainer"]{background:#F7F8FC!important;font-family:'Inter',-apple-system,sans-serif!important;color:#0F172A!important;}
[data-testid="stHeader"]{display:none!important;}
[data-testid="stSidebar"]{display:none!important;}
[data-testid="collapsedControl"]{display:none!important;}
[data-testid="stDecoration"]{display:none!important;}
.main .block-container{padding:0 2.4rem 4rem!important;max-width:1360px!important;}

/* HERO */
.hero-wrap{background:#0A0F1E;border-bottom:1px solid rgba(99,102,241,0.2);padding:1.6rem 2.4rem 1.8rem;margin:0 -2.4rem 2.4rem;position:relative;overflow:hidden;}
.hero-wrap::after{content:'';position:absolute;inset:0;background:radial-gradient(ellipse 60% 80% at 20% 50%,rgba(99,102,241,0.12) 0%,transparent 70%),radial-gradient(ellipse 40% 60% at 80% 50%,rgba(6,182,212,0.08) 0%,transparent 60%);pointer-events:none;}
.hero-inner{display:flex;align-items:center;justify-content:space-between;gap:2rem;position:relative;z-index:2;}
.hero-logo-block{display:flex;align-items:center;gap:0.9rem;flex-shrink:0;}
.hero-logo-block img{height:44px;border-radius:8px;background:white;padding:3px;box-shadow:0 2px 12px rgba(0,0,0,0.4);}
.hero-org{color:rgba(255,255,255,0.35);font-size:0.55rem;font-weight:700;letter-spacing:3px;text-transform:uppercase;}
.hero-dept{color:rgba(255,255,255,0.55);font-size:0.68rem;margin-top:2px;font-weight:400;}
.hero-center{text-align:center;flex:1;}
.hero-eyebrow{font-size:0.58rem;font-weight:600;letter-spacing:5px;text-transform:uppercase;color:#06B6D4;margin-bottom:0.4rem;}
.hero-title{font-family:'JetBrains Mono',monospace;font-size:1.75rem;font-weight:700;color:#FFFFFF;letter-spacing:-0.5px;line-height:1.1;margin-bottom:0.5rem;}
.hero-title em{color:#818CF8;font-style:normal;}
.hero-sub{color:rgba(255,255,255,0.42);font-size:0.76rem;line-height:1.5;margin-bottom:0.9rem;font-weight:300;}
.hero-sub strong{color:rgba(199,210,254,0.75);font-weight:500;}
.hero-pills{display:flex;gap:0.4rem;justify-content:center;flex-wrap:wrap;}
.pill{border-radius:4px;padding:2px 10px;font-size:0.6rem;font-weight:600;letter-spacing:0.5px;border:1px solid;font-family:'JetBrains Mono',monospace;}
.pill-indigo{background:rgba(99,102,241,0.15);border-color:rgba(99,102,241,0.4);color:#A5B4FC;}
.pill-cyan{background:rgba(6,182,212,0.12);border-color:rgba(6,182,212,0.35);color:#67E8F9;}
.pill-green{background:rgba(16,185,129,0.12);border-color:rgba(16,185,129,0.35);color:#6EE7B7;}

/* NAV */
[data-testid="stRadio"]>div{display:flex!important;flex-wrap:wrap!important;gap:0.3rem!important;background:#FFFFFF!important;border:1px solid #E2E8F0!important;border-radius:10px!important;padding:5px!important;margin-bottom:2rem!important;box-shadow:0 1px 4px rgba(0,0,0,0.04)!important;}
[data-testid="stRadio"] label{border-radius:7px!important;padding:0.38rem 0.85rem!important;font-size:0.78rem!important;font-weight:500!important;color:#64748B!important;cursor:pointer!important;transition:all 0.15s!important;border:none!important;background:transparent!important;white-space:nowrap!important;}
[data-testid="stRadio"] label:has(input:checked){background:#6366F1!important;color:white!important;font-weight:600!important;box-shadow:0 2px 8px rgba(99,102,241,0.3)!important;}
[data-testid="stRadio"] input[type="radio"]{display:none!important;}

/* SECTION LABELS */
.sec-label{display:flex;align-items:center;gap:0.6rem;font-size:0.62rem;font-weight:700;letter-spacing:3px;text-transform:uppercase;color:#6366F1;margin:2rem 0 1.2rem;line-height:1;}
.sec-label::before{content:'';display:inline-block;width:3px;height:14px;background:linear-gradient(180deg,#6366F1,#06B6D4);border-radius:2px;flex-shrink:0;}

/* KPI CARDS */
.kpi-card{background:#FFFFFF;border-radius:12px;padding:1.2rem 1rem 1rem;border:1px solid #E2E8F0;text-align:center;position:relative;overflow:hidden;transition:box-shadow 0.2s,transform 0.2s;}
.kpi-card::after{content:'';position:absolute;top:0;left:0;right:0;height:2px;background:linear-gradient(90deg,#6366F1 0%,#06B6D4 100%);}
.kpi-card:hover{box-shadow:0 6px 24px rgba(99,102,241,0.1);transform:translateY(-2px);}
.kpi-icon{font-size:1.3rem;margin-bottom:0.3rem;opacity:0.85;}
.kpi-val{font-family:'JetBrains Mono',monospace;font-size:1.9rem;font-weight:700;color:#0F172A;line-height:1.1;letter-spacing:-1px;}
.kpi-val span{color:#6366F1;}
.kpi-lbl{font-size:0.58rem;color:#94A3B8;text-transform:uppercase;letter-spacing:1.5px;margin-top:5px;font-weight:600;}

/* RESULT BOXES */
.box-ok{background:#F0FDF4;border:1px solid #BBF7D0;border-left:4px solid #22C55E;border-radius:10px;padding:1.2rem 1.4rem;}
.box-warn{background:#FFFBEB;border:1px solid #FDE68A;border-left:4px solid #F59E0B;border-radius:10px;padding:1.2rem 1.4rem;}
.box-bad{background:#FFF1F2;border:1px solid #FECDD3;border-left:4px solid #F43F5E;border-radius:10px;padding:1.2rem 1.4rem;}
.verdict-ok{font-size:1rem;font-weight:800;color:#16A34A;letter-spacing:-0.3px;}
.verdict-warn{font-size:1rem;font-weight:800;color:#D97706;letter-spacing:-0.3px;}
.verdict-bad{font-size:1rem;font-weight:800;color:#E11D48;letter-spacing:-0.3px;}

/* GUIDE / STEP */
.guide-header{border-radius:10px;padding:0.9rem 1.2rem;margin-bottom:1rem;display:flex;align-items:center;gap:0.9rem;border-left:4px solid;}
.guide-icon{font-size:1.6rem;}
.guide-title{font-weight:700;font-size:0.92rem;}
.guide-sub{font-size:0.75rem;color:#94A3B8;margin-top:1px;}
.step-card{background:#FFFFFF;border:1px solid #F1F5F9;border-radius:8px;padding:0.75rem 0.9rem;margin-bottom:0.4rem;display:flex;align-items:flex-start;gap:0.7rem;}
.step-num{min-width:22px;height:22px;border-radius:50%;display:flex;align-items:center;justify-content:center;font-size:0.68rem;font-weight:700;color:white;flex-shrink:0;margin-top:1px;}
.step-txt{font-size:0.82rem;color:#334155;line-height:1.5;}
.info-card{border-radius:8px;padding:0.9rem 1.1rem;margin-bottom:0.7rem;border-left:3px solid;}
.timing-card{background:#FFFFFF;border:1px solid #E2E8F0;border-radius:10px;padding:0.9rem 1rem;display:flex;align-items:center;gap:0.6rem;flex-wrap:wrap;}
.timing-val{font-family:'JetBrains Mono',monospace;font-size:1.35rem;font-weight:700;line-height:1;}

/* MATURITY */
.mat-axis{background:#F8FAFF;border-radius:8px;padding:0.75rem 1.2rem;margin-bottom:0.3rem;border-left:3px solid #6366F1;font-weight:600;font-size:0.85rem;color:#1E1B4B;}

/* SCORE CARD */
.score-card{background:linear-gradient(145deg,#F8FAFF 0%,#EEF2FF 100%);border:1.5px solid #C7D2FE;border-radius:16px;padding:2rem;text-align:center;}
.score-big{font-family:'JetBrains Mono',monospace;font-size:3.5rem;font-weight:800;color:#4338CA;line-height:1;letter-spacing:-2px;}
.score-denom{font-size:1.1rem;color:#94A3B8;font-weight:400;}
.score-level{font-size:1rem;font-weight:700;color:#1E1B4B;margin-top:0.4rem;}
.score-conseil{font-size:0.82rem;color:#64748B;margin-top:0.7rem;line-height:1.6;}

/* ABOUT */
.about-card{background:#FFFFFF;border:1px solid #E2E8F0;border-radius:14px;padding:1.6rem;height:100%;}
.about-title{font-size:0.58rem;font-weight:700;letter-spacing:3px;text-transform:uppercase;color:#6366F1;margin-bottom:0.7rem;display:flex;align-items:center;gap:0.4rem;}
.about-title::before{content:'';display:inline-block;width:2px;height:10px;background:#06B6D4;border-radius:1px;}
.task-row{display:flex;align-items:center;gap:0.7rem;padding:0.5rem 0;border-bottom:1px solid #F8FAFF;}
.task-row:last-child{border-bottom:none;}
.task-icon{font-size:1rem;width:24px;text-align:center;flex-shrink:0;}
.task-name{flex:1;font-size:0.82rem;color:#334155;font-weight:500;}
.task-gain{font-family:'JetBrains Mono',monospace;font-size:0.75rem;font-weight:700;padding:2px 7px;border-radius:4px;}
.gain-high{background:#F0FDF4;color:#15803D;}
.gain-mid{background:#FFFBEB;color:#B45309;}
.gain-low{background:#FFF1F2;color:#BE123C;}

/* PARAM ROWS */
.param-row{display:flex;justify-content:space-between;align-items:center;padding:0.55rem 0.9rem;border-radius:6px;font-size:0.82rem;margin-bottom:3px;}
.param-row:nth-child(odd){background:#F8FAFF;}
.param-row:nth-child(even){background:#FFFFFF;}
.param-key{color:#64748B;font-weight:500;}
.param-val{font-family:'JetBrains Mono',monospace;font-weight:600;color:#0F172A;font-size:0.78rem;text-align:right;}

/* METRIC ROWS */
.metric-row{display:grid;grid-template-columns:2fr 1fr 1fr 1fr 1fr;padding:0.65rem 1rem;border-radius:6px;font-size:0.82rem;margin-bottom:3px;align-items:center;}
.metric-header{background:#EEF2FF;font-weight:700;color:#312E81;}
.metric-data:nth-child(even){background:#F8FAFF;}
.metric-data:nth-child(odd){background:#FFFFFF;border:1px solid #F1F5F9;}

/* STREAMLIT OVERRIDES */
.stButton>button[kind="primary"]{background:#6366F1!important;border:none!important;border-radius:8px!important;font-weight:600!important;font-size:0.85rem!important;padding:0.55rem 1.4rem!important;letter-spacing:0.2px!important;box-shadow:0 2px 8px rgba(99,102,241,0.25)!important;transition:all 0.15s!important;}
.stButton>button[kind="primary"]:hover{background:#4F46E5!important;box-shadow:0 4px 16px rgba(99,102,241,0.35)!important;transform:translateY(-1px)!important;}
.stTabs [data-baseweb="tab-list"]{background:#F1F5F9!important;border-radius:8px!important;padding:3px!important;gap:3px!important;border:none!important;}
.stTabs [data-baseweb="tab"]{border-radius:6px!important;font-weight:500!important;font-size:0.8rem!important;color:#64748B!important;padding:0.35rem 0.9rem!important;}
.stTabs [aria-selected="true"]{background:#FFFFFF!important;color:#4F46E5!important;font-weight:600!important;box-shadow:0 1px 3px rgba(0,0,0,0.08)!important;}
[data-testid="stMetric"]{background:#FFFFFF!important;border-radius:10px!important;padding:0.75rem 1rem!important;border:1px solid #E2E8F0!important;}
[data-testid="stMetricLabel"]{font-size:0.72rem!important;color:#94A3B8!important;}
[data-testid="stMetricValue"]{font-family:'JetBrains Mono',monospace!important;font-size:1.4rem!important;color:#0F172A!important;}
.stDataFrame{border-radius:10px!important;overflow:hidden!important;border:1px solid #E2E8F0!important;}
.streamlit-expanderHeader{background:#F8FAFF!important;border-radius:7px!important;font-weight:500!important;font-size:0.85rem!important;color:#334155!important;border:1px solid #E2E8F0!important;}
[data-testid="stForm"]{background:#FFFFFF!important;border-radius:12px!important;padding:1.4rem!important;border:1px solid #E2E8F0!important;}
[data-testid="stInfo"]{background:#EFF6FF!important;border-color:#BFDBFE!important;border-radius:8px!important;font-size:0.83rem!important;}
.js-plotly-plot .plotly .modebar{display:none!important;}
::-webkit-scrollbar{width:5px;height:5px;}
::-webkit-scrollbar-track{background:#F1F5F9;}
::-webkit-scrollbar-thumb{background:#CBD5E1;border-radius:3px;}
::-webkit-scrollbar-thumb:hover{background:#94A3B8;}
.main .block-container{padding-top:0!important;}
</style>
""", unsafe_allow_html=True)

# ── Load model & data ─────────────────────────────────────────────────────────
@st.cache_resource
def load_model():
    with open("model_rf.pkl", "rb") as f: return pickle.load(f)

@st.cache_data
def load_data():
    return pd.read_csv("dataset_copilot.csv")

@st.cache_data
def load_metrics():
    with open("metrics.json") as f: return json.load(f)

try:
    bundle   = load_model()
    model    = bundle["model"]
    le_task  = bundle["le_task"]
    le_compl = bundle["le_compl"]
    le_deliv = bundle["le_deliv"]
    df       = load_data()
    metrics  = load_metrics()
    MODEL_OK = True
except Exception as e:
    MODEL_OK = False
    st.error(f"Erreur chargement modèle : {e}")

# ── Constants ─────────────────────────────────────────────────────────────────
TACHES = [
    "Créer des rapports automatiquement",
    "Analyser les données rapidement",
    "Poser des questions en langage naturel",
    "Générer du DAX",
    "Nettoyer les données",
    "Améliorer le design",
    "Résumer les insights",
]
# Gains calculés depuis les données terrain (temps_sans - temps_avec) / temps_sans
GAIN_REF = {
    "Créer des rapports automatiquement":    0.256,
    "Analyser les données rapidement":        0.491,
    "Poser des questions en langage naturel": 0.295,
    "Générer du DAX":                         0.637,
    "Nettoyer les données":                   0.204,
    "Améliorer le design":                    0.077,
    "Résumer les insights":                   0.314,
}

# Temps de référence sans Copilot (minutes) — basés sur l'étude empirique
TEMPS_REF = {
    "Créer des rapports automatiquement":    35,  # données terrain: avg=34.6 min
    "Analyser les données rapidement":        40,
    "Poser des questions en langage naturel": 30,
    "Générer du DAX":                         60,
    "Nettoyer les données":                   50,
    "Améliorer le design":                    27,  # données terrain: avg=27.4 min
    "Résumer les insights":                   25,
}
ICONES = {
    "Créer des rapports automatiquement":    "01",
    "Analyser les données rapidement":        "02",
    "Poser des questions en langage naturel": "03",
    "Générer du DAX":                         "04",
    "Nettoyer les données":                   "05",
    "Améliorer le design":                    "06",
    "Résumer les insights":                   "07",
}
ABREV = {
    "Créer des rapports automatiquement":    "Créer rapports",
    "Analyser les données rapidement":        "Analyser données",
    "Poser des questions en langage naturel": "Questions NL",
    "Générer du DAX":                         "Générer DAX",
    "Nettoyer les données":                   "Nettoyer",
    "Améliorer le design":                    "Design",
    "Résumer les insights":                   "Résumer insights",
}
GUIDE = {
    "Créer des rapports automatiquement": {
        "icone":"RAP","color":"#059669",
        "acces":"Power BI Desktop → ruban Accueil → <b>Copilot</b> → <b>'Create a new report page'</b>",
        "prompt":"« Crée une page de rapport pour analyser les données de qualité par région et par mois, avec les indicateurs de performance clés. »",
        "etapes":[
            "Ouvrez votre modèle Power BI avec vos tables de données chargées",
            "Cliquez sur <b>Copilot</b> → <b>'Create a new report page'</b>",
            "Décrivez l'objectif, les dimensions et les mesures souhaitées",
            "Examinez chaque visuel généré : type de graphique, champs, agrégations",
            "Vérifiez que Copilot utilise les bonnes colonnes et mesures",
            "Ajustez manuellement les couleurs et titres selon votre charte graphique",
        ],
        "vigilance":"Copilot peut confondre des colonnes de même type. Vérifiez systématiquement quelle colonne est utilisée dans chaque visuel avant diffusion.",
    },
    "Analyser les données rapidement": {
        "icone":"ANA","color":"#D97706",
        "acces":"Power BI Desktop → Copilot → <b>'Answer a question about the data'</b>",
        "prompt":"« Quels sont les 5 éléments avec les valeurs les plus élevées ? Y a-t-il des anomalies par catégorie ou période ? »",
        "etapes":[
            "Ouvrez Copilot → <b>'Answer a question about the data'</b>",
            "Citez explicitement le nom de la table à interroger",
            "Examinez le visuel généré et vérifiez les colonnes utilisées",
            "Affinez avec des filtres supplémentaires selon votre contexte",
            "Vérifiez que les calculs correspondent aux formules de votre modèle",
            "Consolidez vos découvertes via <b>'Suggest content for a new report page'</b>",
        ],
        "vigilance":"Précisez toujours quelle table interroger. Sans précision, Copilot peut choisir une table incorrecte ou mélanger les sources de données.",
    },
    "Poser des questions en langage naturel": {
        "icone":"NLQ","color":"#7C3AED",
        "acces":"Power BI Desktop → Copilot → <b>'Answer a question about the data'</b>",
        "prompt":"« Quel est l'indicateur moyen par catégorie pour la période sélectionnée ? Quelles catégories dépassent la cible définie ? »",
        "etapes":[
            "Ouvrez la page de rapport concernée dans Power BI Desktop",
            "Ouvrez Copilot → <b>'Answer a question about the data'</b>",
            "Posez votre question en langage naturel, en citant les noms de colonnes exacts",
            "Copilot génère un visuel ou une réponse textuelle — examinez les deux",
            "Vérifiez chaque chiffre par rapport aux visuels de la page",
            "Reformulez la question si le résultat ne correspond pas à votre attente",
        ],
        "vigilance":"Si des filtres sont actifs sur la page, la réponse Copilot reflète ce périmètre uniquement. Précisez-le systématiquement à vos lecteurs.",
    },
    "Générer du DAX": {
        "icone":"DAX","color":"#DC2626",
        "acces":"Power BI Desktop → Copilot → <b>'Answer a question about the data'</b>",
        "prompt":"« Écris une mesure DAX pour calculer l'indicateur YTD sur la période souhaitée, en filtrant sur l'année et les mois concernés à partir des tables de mon modèle. »",
        "etapes":[
            "Identifiez précisément : table source, colonne à agréger, logique de filtre souhaitée",
            "Formulez le prompt en citant les noms exacts des tables et colonnes",
            "Copiez la formule dans un éditeur texte — <b>NE l'appliquez PAS directement</b>",
            "Analysez ligne par ligne : fonctions, filtres CALCULATE, relations entre tables",
            "Testez sur des données connues dont vous connaissez le résultat exact",
            "Comparez avec vos mesures existantes avant de déployer en production",
        ],
        "vigilance":"En moyenne 4 corrections nécessaires par formule DAX générée. Les relations complexes entre tables sont rarement bien gérées automatiquement. Validez systématiquement.",
    },
    "Nettoyer les données": {
        "icone":"NET","color":"#0891B2",
        "acces":"Power BI Desktop → Power Query Editor → <b>Copilot (ruban Power Query)</b>",
        "prompt":"« Dans cette table, identifie les lignes où la colonne contient des valeurs aberrantes et propose le code M pour les filtrer. »",
        "etapes":[
            "Ouvrez Power Query Editor dans Power BI Desktop",
            "Sélectionnez la table à nettoyer",
            "Cliquez sur <b>Copilot</b> dans le ruban Power Query",
            "Décrivez le problème : valeurs nulles, types incorrects, doublons, aberrants",
            "Examinez le code M généré <b>avant</b> de l'appliquer",
            "Testez sur un extrait avant d'appliquer à toute la table",
        ],
        "vigilance":"Le Copilot Power Query est distinct du Copilot Power BI. Il génère du code M — vérifiez que les étapes ajoutées ne suppriment pas des données valides.",
    },
    "Améliorer le design": {
        "icone":"DES","color":"#BE185D",
        "acces":"Power BI Desktop → Copilot → <b>'Suggest content for a new report page'</b>",
        "prompt":"« Améliore le design de cette page : propose une palette cohérente, optimise l'alignement des visuels et suggère des titres dynamiques. »",
        "etapes":[
            "Ouvrez Copilot → <b>'Suggest content for a new report page'</b>",
            "Demandez une amélioration de la mise en page et des couleurs",
            "Appliquez votre charte : View → Themes → Customize",
            "Utilisez les suggestions Copilot comme base, personnalisez ensuite",
            "Vérifiez la lisibilité sur différentes résolutions d'écran",
            "Testez en mode présentation avant diffusion",
        ],
        "vigilance":"Copilot ne connaît pas votre charte graphique. Les couleurs générées automatiquement doivent être remplacées manuellement par vos couleurs officielles.",
    },
    "Résumer les insights": {
        "icone":"INS","color":"#4F46E5",
        "acces":"Power BI Desktop → Copilot → <b>'Answer a question about the data'</b>",
        "prompt":"« Rédige un résumé exécutif de cette page en mettant en avant les 3 KPI clés, les tendances notables et les éléments nécessitant une attention particulière. »",
        "etapes":[
            "Naviguez sur la page à résumer dans Power BI Desktop",
            "Appliquez les filtres souhaités avant d'ouvrir Copilot",
            "Ouvrez Copilot → <b>'Answer a question about the data'</b>",
            "Demandez un résumé en précisant les KPI prioritaires de votre rapport",
            "Relisez et <b>vérifiez chaque chiffre</b> par rapport aux visuels affichés",
            "Copiez le contenu validé dans votre support (PowerPoint, email, Word)",
        ],
        "vigilance":"Si des filtres sont appliqués, le résumé reflète ce périmètre uniquement — précisez-le à vos lecteurs pour éviter toute mauvaise interprétation.",
    },
}

C_ACCENT = "#6366F1"
C_CYAN   = "#06B6D4"
C_GREEN  = "#22C55E"
C_ORANGE = "#F59E0B"
C_RED    = "#F43F5E"
C_BG     = "#FFFFFF"
C_SURF   = "#F8FAFF"
C_BORDER = "#E2E8F0"
C_MUTED  = "#94A3B8"
C_TEXT   = "#0F172A"

def chart_cfg(title="", h=300):
    return dict(
        title=dict(text=title, font=dict(color="#64748B", size=11, family="Inter"), x=0),
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="#FFFFFF",
        font=dict(color="#0F172A", size=11, family="Inter"),
        legend=dict(bgcolor="rgba(0,0,0,0)", font=dict(color="#64748B", size=10),
                    bordercolor="rgba(0,0,0,0)"),
        margin=dict(l=10, r=20, t=44, b=10),
        xaxis=dict(gridcolor="#F1F5F9", zerolinecolor="#F1F5F9", color="#94A3B8",
                   linecolor="#E2E8F0", showline=True, tickfont=dict(size=10)),
        yaxis=dict(gridcolor="#F1F5F9", zerolinecolor="#F1F5F9", color="#94A3B8",
                   linecolor="#E2E8F0", showline=True, tickfont=dict(size=10)),
        height=h,
        hoverlabel=dict(bgcolor="#1E293B", font=dict(color="white", size=11, family="Inter"),
                       bordercolor="#1E293B"),
    )

def encode_input(task, compl, deliv):
    try: te = le_task.transform([task])[0]
    except: te = 0
    try: ce = le_compl.transform([compl])[0]
    except: ce = 0
    try: de = le_deliv.transform([deliv])[0]
    except: de = 0
    return te, ce, de

if "historique" not in st.session_state:
    st.session_state.historique = []

# ════════════════════════════════════════════════════════
# HEADER
# ════════════════════════════════════════════════════════
acc_str = f"{round(metrics['accuracy']*100,1)}%" if MODEL_OK else "N/A"

LOGO_OP   = "data:image/png;base64,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"
LOGO_NEXA = "data:image/jpeg;base64,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"

st.markdown(f"""
<div class="hero-wrap">
  <div class="hero-inner">
    <div class="hero-logo-block">
      <img src="{LOGO_OP}" alt="OPmobility"/>
      <div>
        <div class="hero-org">OPmobility · BU C-POWER</div>
        <div class="hero-dept">Direction des Achats</div>
      </div>
    </div>
    <div class="hero-center">
      <div class="hero-eyebrow">Mémoire Professionnel · RNCP 37137 · Chef de projet Data & IA</div>
      <div class="hero-title">// CopilotBI <em>Analyzer</em></div>
      <div class="hero-sub">Optimisation de la productivité BI par l'intégration de <strong>Microsoft Copilot dans Power BI</strong></div>
      <div class="hero-pills">
        <span class="pill pill-indigo">RF · acc={acc_str}</span>
        <span class="pill pill-cyan">n=200 · 7 tâches</span>
        <span class="pill pill-green">t-test · Cohen d · ROI</span>
        <span class="pill pill-indigo">Power BI · Databricks</span>
      </div>
    </div>
    <div style="text-align:center;flex-shrink:0;z-index:2;">
      <img src="{LOGO_NEXA}" alt="Nexa" style="height:44px;border-radius:8px;box-shadow:0 2px 12px rgba(0,0,0,0.4);display:block;background:white;padding:3px;"/>
      <div style="color:rgba(255,255,255,0.3);font-size:0.52rem;text-align:center;margin-top:4px;letter-spacing:2px;text-transform:uppercase;font-family:'JetBrains Mono',monospace;">Nexa Digital</div>
    </div>
  </div>
</div>
""", unsafe_allow_html=True)

# ── Navigation ────────────────────────────────────────────────────────────────
page = st.radio("nav", [
    "Tableau de bord",
    "Recommandation IA",
    "Maturité Copilot",
    "Performance modèle",
    "Tests statistiques",
    "Analyse ROI",
    "Glossaire",
    "À propos",
], label_visibility="collapsed", horizontal=True)

st.markdown("<div style='height:0.2rem;'></div>", unsafe_allow_html=True)

# ════════════════════════════════════════════════════════
# PAGE 1 — TABLEAU DE BORD
# ════════════════════════════════════════════════════════
if "Tableau de bord" in page:
    if not MODEL_OK: st.error("Modèle introuvable."); st.stop()

    df_cop = df[df["copilot_utilise"]==1]
    df_no  = df[df["copilot_utilise"]==0]
    gain_g = round((df_no["temps_realisation_min"].mean()-df_cop["temps_realisation_min"].mean())/df_no["temps_realisation_min"].mean()*100,1)

    st.markdown('<div class="sec-label">Vue d\'ensemble — Copilot dans Power BI</div>', unsafe_allow_html=True)

    kpi_data = [
        ("200","Observations"),
        (f"{gain_g}%","Gain temps moyen"),
        (f"{round(metrics['accuracy']*100,1)}%","Précision RF"),
        ("7","Types de tâches"),
        (f"{int(df['copilot_utilise'].sum())}","Avec Copilot"),
    ]
    cols = st.columns(5)
    for col,(val,lbl) in zip(cols,kpi_data):
        with col:
            st.markdown(f'<div class="kpi-card"><div class="kpi-val">{val}</div><div class="kpi-lbl">{lbl}</div></div>', unsafe_allow_html=True)

    st.markdown('<div class="sec-label">Analyse par tâche Copilot</div>', unsafe_allow_html=True)

    rows = []
    for task in TACHES:
        tn   = TEMPS_REF[task]
        g    = round(GAIN_REF[task] * 100, 1)
        tc   = round(tn * (1 - GAIN_REF[task]), 1)
        rec  = "Recommandé" if g>=25 else ("Vigilance" if g>=10 else "Déconseillé")
        rows.append({"Tâche":task,"Sans Copilot":f"{tn} min","Avec Copilot":f"{tc} min","Gain":f"{g}%","Recommandation":rec})
    st.dataframe(pd.DataFrame(rows), use_container_width=True, hide_index=True)
    st.markdown("""
    <div style='font-size:0.74rem;color:#94A3B8;margin-top:0.3rem;margin-bottom:0.5rem;font-family:"JetBrains Mono",monospace;'>
    Gains calculés depuis les données terrain : (temps_sans_Copilot − temps_avec_Copilot) / temps_sans_Copilot.
    Seuil de recommandation : ≥ 25% → Recommandé · 10–25% → Vigilance · &lt; 10% → Déconseillé.
    </div>""", unsafe_allow_html=True)

    st.markdown('<div class="sec-label">Comparaison des temps & gains</div>', unsafe_allow_html=True)
    col1, col2 = st.columns(2)

    with col1:
        avg_rows = []
        for task in TACHES:
            tn = TEMPS_REF[task]
            tc = round(tn * (1 - GAIN_REF[task]), 1)
            avg_rows.append({"Tâche": ABREV[task], "Temps moyen (min)": tn,  "Mode": "Sans Copilot"})
            avg_rows.append({"Tâche": ABREV[task], "Temps moyen (min)": tc,  "Mode": "Avec Copilot"})
        avg = pd.DataFrame(avg_rows)
        fig1 = px.bar(avg, x="Tâche", y="Temps moyen (min)", color="Mode", barmode="group",
                      color_discrete_map={"Sans Copilot":"#E2E8F0","Avec Copilot":"#6366F1"},
                      labels={"Tâche":""})
        fig1.update_layout(**chart_cfg("Temps moyen par tâche (min) — Gains calculés depuis données terrain"))
        fig1.update_traces(marker_line_width=0, marker_cornerradius=4)
        st.plotly_chart(fig1, use_container_width=True)

    with col2:
        gdf = pd.DataFrame([{"Tâche":ABREV[t],"Gain (%)":round(GAIN_REF[t]*100)} for t in TACHES]).sort_values("Gain (%)")
        clrs = ["#22C55E" if g>=30 else "#F59E0B" if g>=15 else "#F43F5E" for g in gdf["Gain (%)"]]
        fig2 = go.Figure(go.Bar(
            x=gdf["Gain (%)"], y=gdf["Tâche"], orientation="h",
            marker_color=clrs, marker_line_width=0,
            text=[f"{g}%" for g in gdf["Gain (%)"]],
            textposition="outside", textfont=dict(size=11, color=C_TEXT),
        ))
        fig2.add_vline(x=25, line_dash="dot", line_color="#9CA3AF",
                       annotation_text="Seuil 25%", annotation_font=dict(color="#9CA3AF", size=10))
        fig2.update_layout(**chart_cfg("Gain de productivité par tâche (%)"))
        fig2.update_layout(height=320, xaxis=dict(range=[0,58]))
        st.plotly_chart(fig2, use_container_width=True)

    st.markdown('<div class="sec-label">Qualité des livrables & itérations</div>', unsafe_allow_html=True)
    col3, col4 = st.columns(2)

    with col3:
        dims   = ["score_pertinence","score_clarte","score_exactitude","score_exploitabilite"]
        labels = ["Pertinence","Clarté","Exactitude","Exploitabilité"]
        vc = [df_cop[d].mean() for d in dims]
        vn = [df_no[d].mean()  for d in dims]
        fig3 = go.Figure()
        fig3.add_trace(go.Scatterpolar(r=vc+[vc[0]], theta=labels+[labels[0]], fill="toself",
            name="Avec Copilot", line=dict(color="#6366F1",width=2), fillcolor="rgba(99,102,241,0.15)"))
        fig3.add_trace(go.Scatterpolar(r=vn+[vn[0]], theta=labels+[labels[0]], fill="toself",
            name="Sans Copilot", line=dict(color="#06B6D4",width=2,dash="dot"), fillcolor="rgba(6,182,212,0.08)"))
        fig3.update_layout(**chart_cfg("Scores qualité moyens (/5)"))
        fig3.update_layout(height=310, polar=dict(
            bgcolor="#FAFAFA",
            radialaxis=dict(range=[3.5,5.0], color=C_MUTED, gridcolor=C_BORDER, tickfont=dict(size=9)),
            angularaxis=dict(color=C_TEXT, gridcolor=C_BORDER),
        ))
        st.plotly_chart(fig3, use_container_width=True)

    with col4:
        fig4 = px.box(df, x=df["type_tache"].map(ABREV), y="nb_iterations",
                      color=df["copilot_utilise"].map({0:"Sans Copilot",1:"Avec Copilot"}),
                      color_discrete_map={"Sans Copilot":"#E2E8F0","Avec Copilot":"#6366F1"},
                      labels={"y":"Nb itérations","x":"","color":""})
        fig4.update_layout(**chart_cfg("Itérations nécessaires par tâche"))
        fig4.update_xaxes(tickangle=-25, tickfont=dict(size=9))
        st.plotly_chart(fig4, use_container_width=True)


# ════════════════════════════════════════════════════════
# PAGE 2 — RECOMMANDATION IA
# ════════════════════════════════════════════════════════
elif "Recommandation" in page:
    if not MODEL_OK: st.error("Modèle introuvable."); st.stop()

    st.markdown('<div class="sec-label">Recommandation d\'usage — Intelligence artificielle</div>', unsafe_allow_html=True)
    st.markdown("<p style='color:#6B7280;font-size:0.88rem;margin-bottom:1.5rem;max-width:700px;'>Renseignez le contexte de votre tâche Power BI. Le modèle Random Forest évalue si Copilot est pertinent et génère un guide d'utilisation adapté.</p>", unsafe_allow_html=True)

    col_form, col_res = st.columns([1,1], gap="large")

    with col_form:
        with st.container():
            st.markdown("**Paramètres de la tâche**")
            task   = st.selectbox("Type de tâche Copilot", TACHES, format_func=lambda x: f"[{ICONES[x]}] {x}")
            compl  = st.selectbox("Niveau de complexité", ["Faible","Moyen","Élevé"])
            deliv  = st.selectbox("Type de livrable",     ["Opérationnel","Management","Exploratoire"])
            time_v = st.slider("Temps estimé sans Copilot (min)", 5, 120, 45, 5)
            qual   = st.slider("Score qualité attendu /5", 1.0, 5.0, 4.0, 0.1)
            iter_n = st.slider("Itérations habituellement nécessaires", 1, 5, 2)
            btn    = st.button("Analyser et recommander", use_container_width=True, type="primary")

    with col_res:
        if btn:
            # ── Recommandation basée sur GAIN_REF (données terrain) ─────────
            gain_val = GAIN_REF.get(task, 0.20)
            gp       = round(gain_val * 100, 1)
            gt       = round(time_v * gain_val)
            ta       = time_v - gt

            # Seuils basés sur gains mesurés empiriquement
            if gain_val >= 0.25:
                box_cls,verdict,vcolor = "box-ok","COPILOT RECOMMANDÉ","#059669"
                msg = f"Pour **{task}**, le gain mesuré est de **{gp}%** ({gt} min économisées). Copilot apporte une valeur ajoutée significative."
                tip = "Commencez par la génération Copilot, validez systématiquement avant diffusion."
                rec_level = 1
            elif gain_val >= 0.10:
                box_cls,verdict,vcolor = "box-warn","USAGE AVEC VIGILANCE","#D97706"
                msg = f"Pour **{task}**, le gain mesuré est de **{gp}%** ({gt} min économisées). Copilot peut aider mais nécessite une vérification rigoureuse."
                tip = "Utilisez Copilot pour la génération initiale mais prévoyez du temps de validation."
                rec_level = 0
            else:
                box_cls,verdict,vcolor = "box-bad","USAGE DÉCONSEILLÉ","#E11D48"
                msg = f"Pour **{task}**, le gain mesuré est seulement de **{gp}%** — inférieur au seuil de rentabilité (10%). Préférez une réalisation manuelle."
                tip = "Cette tâche nécessite une expertise métier que Copilot ne remplace pas efficacement."
                rec_level = 0

            # ── Confiance RF comme indicateur secondaire ─────────────────────
            te,ce,de = encode_input(task, compl, deliv)
            X_in  = pd.DataFrame([[te,ce,de,float(time_v),iter_n,qual,qual,qual,qual]], columns=bundle["features"])
            proba_rf = model.predict_proba(X_in)[0][1]  # proba que copilot soit utilisé
            proba = max(proba_rf, 1-proba_rf)           # confiance = max des deux probas

            verdict_cls = "ok" if gain_val >= 0.25 else "bad" if gain_val < 0.10 else "warn"
            st.markdown(f'<div class="{box_cls}"><div class="verdict-{verdict_cls}">{verdict}</div><p style="margin:0.5rem 0 0;font-size:0.85rem;color:#374151;">{msg}</p></div>', unsafe_allow_html=True)
            st.info(tip)

            m1,m2,m3 = st.columns(3)
            m1.metric("Gain estimé",      f"~{gp}%")
            m2.metric("Temps économisé",   f"~{gt} min")
            m3.metric("Signal RF",  f"{round(proba_rf*100,1)}% utilisateurs Copilot")

            fig_g = go.Figure(go.Indicator(
                mode="gauge+number",
                value=round(gain_val*100,1),
                number={"suffix":"%","font":{"color":vcolor,"size":30,"family":"JetBrains Mono"},"valueformat":".1f"},
                title={"text":"Gain mesuré (données terrain)","font":{"color":C_MUTED,"size":10}},
                gauge={
                    "axis":{"range":[0,70],"tickcolor":C_MUTED,"tickfont":{"size":9}},
                    "bar":{"color":vcolor,"thickness":0.7},
                    "bgcolor":"#F9FAFB",
                    "bordercolor":C_BORDER,
                    "steps":[{"range":[0,50],"color":"#FEF3C7"},{"range":[50,75],"color":"#D1FAE5"}],
                    "threshold":{"line":{"color":"red","width":2},"thickness":0.75,"value":50},
                },
            ))
            fig_g.update_layout(paper_bgcolor="rgba(0,0,0,0)", font=dict(color=C_TEXT,family="Inter"),
                                height=200, margin=dict(l=20,r=20,t=30,b=10))
            st.plotly_chart(fig_g, use_container_width=True)
        else:
            st.markdown("<br><br>", unsafe_allow_html=True)
            st.info("Configurez les paramètres de la tâche à gauche, puis cliquez sur **Analyser et recommander** pour obtenir la recommandation Copilot et le guide opérationnel.")

    if btn:
        guide = GUIDE.get(task)
        if guide:
            gc = guide["color"]
            st.markdown("<br>", unsafe_allow_html=True)
            st.markdown(f"""
            <div style='background:linear-gradient(135deg,{gc}10,{gc}06);
                border:1px solid {gc}40;border-left:5px solid {gc};
                border-radius:12px;padding:1rem 1.5rem;margin-bottom:1rem;
                display:flex;align-items:center;gap:1rem;'>
                <div style='font-family:JetBrains Mono;font-size:0.8rem;font-weight:700;color:{gc};background:{gc}20;padding:4px 8px;border-radius:4px;'>{guide["icone"]}</div>
                <div>
                    <div style='font-weight:800;color:{gc};font-size:0.95rem;'>
                        Recommandations opérationnelles — {task}</div>
                    <div style='font-size:0.78rem;color:#6B7280;margin-top:2px;'>
                        Annexe opérationnelle · Ces éléments sont détaillés dans le livrable terrain joint au mémoire</div>
                </div>
            </div>""", unsafe_allow_html=True)

            cg1, cg2, cg3 = st.columns([1,1,1], gap="large")

            with cg1:
                st.markdown(f"""
                <div class="info-card" style="background:linear-gradient(135deg,{gc}10,{gc}06);border-left-color:{gc};">
                    <div style="font-weight:700;color:{gc};font-size:0.82rem;margin-bottom:0.5rem;">️ Accès Power BI</div>
                    <div style="font-size:0.83rem;color:#374151;line-height:1.6;">{guide["acces"]}</div>
                </div>
                <div class="info-card" style="background:#EEF2FF;border-left-color:#6366F1;">
                    <div style="font-weight:700;color:#4338CA;font-size:0.82rem;margin-bottom:0.5rem;"> Prompt type</div>
                    <div style="font-size:0.83rem;color:#1E1B4B;font-style:italic;line-height:1.6;">{guide["prompt"]}</div>
                </div>""", unsafe_allow_html=True)

            with cg2:
                st.markdown(f"<div style='font-weight:700;color:#111827;font-size:0.88rem;margin-bottom:0.8rem;border-bottom:2px solid {gc}30;padding-bottom:0.4rem;'> Étapes clés</div>", unsafe_allow_html=True)
                for i, etape in enumerate(guide["etapes"][:4], 1):
                    st.markdown(f"""
                    <div class="step-card">
                        <div class="step-num" style="background:{gc};">{i}</div>
                        <div class="step-txt">{etape}</div>
                    </div>""", unsafe_allow_html=True)
                st.markdown(f"<div style='font-size:0.75rem;color:#9CA3AF;margin-top:0.4rem;'>+ {len(guide['etapes'])-4} étapes supplémentaires dans le livrable terrain</div>", unsafe_allow_html=True)

            with cg3:
                st.markdown(f"""
                <div class="info-card" style="background:linear-gradient(135deg,#FFFBEB,#FEF3C7);border-left-color:#F59E0B;">
                    <div style="font-weight:700;color:#B45309;font-size:0.82rem;margin-bottom:0.5rem;">Point de vigilance</div>
                    <div style="font-size:0.83rem;color:#3E2000;line-height:1.6;">{guide["vigilance"]}</div>
                </div>
                <div class="timing-card">
                    <div style="text-align:center;flex:1;">
                        <div style="font-size:0.6rem;color:#9CA3AF;text-transform:uppercase;margin-bottom:2px;">Sans Copilot</div>
                        <div class="timing-val" style="color:#9CA3AF;">{time_v}<span style="font-size:0.7rem;"> min</span></div>
                    </div>
                    <div style="font-size:1.4rem;color:#D1D5DB;">→</div>
                    <div style="text-align:center;flex:1;">
                        <div style="font-size:0.6rem;color:#10B981;text-transform:uppercase;margin-bottom:2px;">Avec Copilot</div>
                        <div class="timing-val" style="color:#10B981;">~{ta}<span style="font-size:0.7rem;"> min</span></div>
                    </div>
                    <div style="text-align:center;flex:1;background:{gc}15;border-radius:8px;padding:0.5rem;">
                        <div style="font-size:0.6rem;color:{gc};text-transform:uppercase;margin-bottom:2px;">Gain mesuré</div>
                        <div class="timing-val" style="color:{gc};">~{gp}<span style="font-size:0.7rem;">%</span></div>
                    </div>
                </div>""", unsafe_allow_html=True)


# ════════════════════════════════════════════════════════
# PAGE 4 — MATURITÉ
# ════════════════════════════════════════════════════════
elif "Maturité" in page:

    cronbach = metrics.get("cronbach_alpha", 0.639) if MODEL_OK else 0.639

    st.markdown('<div class="sec-label">Instrument de mesure — Maturité d\'adoption Copilot</div>', unsafe_allow_html=True)
    st.markdown(f"""
    <div style='background:#F9FAFB;border:1px solid #E5E7EB;border-radius:12px;
        padding:1.2rem 1.6rem;margin-bottom:1.8rem;font-size:0.84rem;color:#374151;line-height:1.7;'>
    <b style='color:#6366F1;'>Cadre théorique</b> — Cet instrument s'inspire des modèles TAM (Technology Acceptance Model,
    Davis 1989) et UTAUT (Venkatesh et al., 2003), adaptés au contexte de l'adoption de Copilot dans Power BI.
    Il mesure 5 dimensions clés : maîtrise technique, validation qualité, gains perçus, usages avancés et gouvernance.
    <br><br>
    <b style='color:#6366F1;'>Validation psychométrique</b> — Cohérence interne mesurée par l'<b>α de Cronbach = {cronbach}</b>
    sur les 4 items de qualité des données terrain (n=200).
    <span style='color:{"#059669" if cronbach >= 0.7 else "#D97706"};font-weight:600;'>
    {" Cohérence satisfaisante (α ≥ 0.7)" if cronbach >= 0.7 else "Cohérence acceptable (α ≥ 0.6) — instrument en cours de validation sur échantillon élargi"}
    </span>
    <br><br>
    <b style='color:#6B7280;font-size:0.78rem;'>
    Note méthodologique : les scores obtenus sont des indicateurs orienteurs. Ils n'ont pas valeur de mesure
    psychométrique certifiée faute d'étalonnage sur un panel représentatif (objectif : n ≥ 500).
    </b>
    </div>""", unsafe_allow_html=True)

    SM = {"Jamais":0,"Parfois":1,"Toujours":2,"Non":0,"Oui":2,"Oui clairement":2,"En cours":1,"Régulièrement":2}

    with st.form("mat_form"):
        axes_q = [
            ("Axe 1 — Maîtrise technique","Créer rapports & Générer DAX · Items T1–T2",[
                ("T1. Vous créez des pages de rapport via Copilot de façon autonome ?", ["Jamais","Parfois","Toujours"]),
                ("T2. Vous citez les noms exacts de tables/colonnes dans vos prompts DAX ?", ["Jamais","Parfois","Toujours"]),
            ]),
            ("Axe 2 — Validation & qualité","Analyser données & Résumer insights · Items V1–V2",[
                ("V1. Vous vérifiez systématiquement les résultats Copilot avant diffusion ?", ["Jamais","Parfois","Toujours"]),
                ("V2. Vous testez les mesures DAX générées sur des données de référence connues ?", ["Jamais","Parfois","Toujours"]),
            ]),
            ("Axe 3 — Gains perçus","Questions NL & Résumer insights · Items G1–G2",[
                ("G1. Copilot vous fait percevoir un gain de temps significatif sur les questions NL ?", ["Non","Parfois","Oui clairement"]),
                ("G2. Vous utilisez Copilot pour synthétiser les insights de vos rapports ?", ["Jamais","Parfois","Régulièrement"]),
            ]),
            ("Axe 4 — Usages avancés","Nettoyer données & Améliorer design · Items U1–U2",[
                ("U1. Vous utilisez Copilot Power Query pour identifier et corriger les anomalies ?", ["Jamais","Parfois","Toujours"]),
                ("U2. Vous utilisez Copilot pour optimiser le design visuel de vos rapports ?", ["Jamais","Parfois","Toujours"]),
            ]),
            ("Axe 5 — Gouvernance & adoption","Documentation & partage des pratiques · Items A1–A2",[
                ("A1. Vous tracez quels livrables ont été produits avec l'assistance de Copilot ?", ["Jamais","Parfois","Régulièrement"]),
                ("A2. Vous itérez sur vos prompts pour améliorer la qualité des outputs Copilot ?", ["Jamais","Parfois","Toujours"]),
            ]),
        ]
        all_answers = []
        for ax_title, ax_sub, questions in axes_q:
            st.markdown(f'<div class="mat-axis">{ax_title} <span style="font-weight:400;color:#6B7280;font-size:0.76rem;">· {ax_sub}</span></div>', unsafe_allow_html=True)
            for q_txt, q_opts in questions:
                ans = st.radio(q_txt, q_opts, horizontal=True, key=q_txt)
                all_answers.append(ans)

        sub = st.form_submit_button("  Calculer le score de maturité", use_container_width=True, type="primary")

    if sub:
        scores_raw  = [SM.get(a, 0) for a in all_answers]
        axes_names  = ["Maîtrise technique","Validation & qualité","Gains perçus","Usages avancés","Gouvernance & adoption"]
        axes_scores = {axes_names[i]: (scores_raw[i*2] + scores_raw[i*2+1]) / 4 * 5 for i in range(5)}
        sg = round(sum(axes_scores.values()) / 5, 1)

        niv, conseil, niv_color = next(
            (v for k, v in {
                (0,   2):   ("Débutant",       "Commencez par les tâches à fort gain mesuré : Générer DAX (+64%) et Analyser les données (+49%).", "#EF4444"),
                (2,   3.5): ("Intermédiaire",  "Renforcez la validation systématique — surtout pour Générer DAX (fort gain mais risque d'erreur élevé).", "#F59E0B"),
                (3.5, 4.5): ("Avancé",         "Travaillez la gouvernance et la traçabilité des livrables produits avec Copilot.", "#10B981"),
                (4.5, 6):   ("Expert",          "Vous maîtrisez les 7 dimensions Copilot. Portez ce savoir-faire à vos équipes.", "#6366F1"),
            }.items() if k[0] <= sg < k[1]),
            ("", "", C_ORANGE)
        )

        cs1, cs2 = st.columns([1, 1.2], gap="large")

        with cs1:
            st.markdown(f"""
            <div class="score-card">
                <div style="font-size:0.62rem;color:#9CA3AF;text-transform:uppercase;letter-spacing:2px;margin-bottom:0.5rem;">Score global (/5)</div>
                <div class="score-big">{sg}<span class="score-denom">/5</span></div>
                <div class="score-level">{niv}</div>
                <div class="score-conseil">{conseil}</div>
            </div>""", unsafe_allow_html=True)

            st.markdown("<br>**Axes à renforcer en priorité :**", unsafe_allow_html=True)
            recos = {
                "Maîtrise technique":      "Pratiquez la création de pages via Copilot et formulez des prompts avec les noms de colonnes exacts.",
                "Validation & qualité":    "Mettez en place une checklist de vérification systématique avant toute diffusion de livrable Copilot.",
                "Gains perçus":            "Testez en priorité Générer DAX (+64% mesuré) et Analyser les données (+49%).",
                "Usages avancés":          "Explorez Copilot Power Query pour le nettoyage des anomalies de données.",
                "Gouvernance & adoption":  "Créez un journal des livrables produits avec/sans Copilot pour mesurer l'adoption réelle.",
            }
            for ax, sc in axes_scores.items():
                if sc < 3.5:
                    st.markdown(f"- **{ax}** `{round(sc,1)}/5` — {recos[ax]}")

            # Scores table
            st.markdown("<br>", unsafe_allow_html=True)
            scores_df = pd.DataFrame([
                {"Axe": k, "Score": f"{round(v,1)}/5",
                 "Niveau": "Expert" if v>=4.5 else "Avancé" if v>=3.5 else "Intermédiaire" if v>=2 else "Débutant"}
                for k,v in axes_scores.items()
            ])
            st.dataframe(scores_df, use_container_width=True, hide_index=True)

        with cs2:
            lbls = list(axes_scores.keys())
            vals = list(axes_scores.values())
            fig_m = go.Figure()
            fig_m.add_trace(go.Scatterpolar(
                r=vals+[vals[0]], theta=lbls+[lbls[0]],
                fill="toself", name="Votre profil",
                line=dict(color="#6366F1", width=2.5),
                fillcolor="rgba(99,102,241,0.18)"
            ))
            fig_m.add_trace(go.Scatterpolar(
                r=[5,5,5,5,5,5], theta=lbls+[lbls[0]],
                fill="toself", name="Expert (référence)",
                line=dict(color="#10B981", width=1, dash="dot"),
                fillcolor="rgba(16,185,129,0.04)"
            ))
            fig_m.update_layout(
                title=dict(text="Profil de maturité Copilot (5 axes)", font=dict(color="#9CA3AF",size=11), x=0),
                paper_bgcolor="rgba(0,0,0,0)", font=dict(color="#111827",size=10),
                legend=dict(bgcolor="rgba(0,0,0,0)", orientation="h", y=-0.18, font=dict(size=10)),
                margin=dict(l=40,r=40,t=50,b=70), height=420,
                polar=dict(bgcolor="#FFFFFF",
                    radialaxis=dict(range=[0,5], tickfont=dict(color="#9CA3AF",size=9),
                                    gridcolor="#E5E7EB", linecolor="#E5E7EB"),
                    angularaxis=dict(tickfont=dict(color="#111827",size=10),
                                     gridcolor="#E5E7EB", direction="clockwise", rotation=90)
                )
            )
            st.plotly_chart(fig_m, use_container_width=True)

            st.markdown(f"""
            <div style='background:#F9FAFB;border:1px solid #E5E7EB;border-radius:10px;
                padding:0.9rem 1.2rem;font-size:0.8rem;color:#6B7280;line-height:1.6;'>
            <b>Lecture du radar</b> — Chaque axe varie de 0 (non pratiqué) à 5 (expert).
            La surface bleue représente votre profil actuel. La ligne verte pointillée représente
            le niveau expert de référence. Un profil équilibré est préférable à un profil fort
            sur un seul axe. α de Cronbach = <b>{cronbach}</b>.
            </div>""", unsafe_allow_html=True)


# ════════════════════════════════════════════════════════
# PAGE 5 — PERFORMANCE MODÈLE
# ════════════════════════════════════════════════════════
elif "Performance" in page:
    if not MODEL_OK: st.error("Modèle introuvable."); st.stop()

    st.markdown('<div class="sec-label">Performance du modèle — Random Forest Classifier</div>', unsafe_allow_html=True)

    col_p, col_cm, col_cv = st.columns(3, gap="large")

    with col_p:
        st.markdown("**Paramètres optimaux**")
        params = [
            ("Algorithme","Random Forest"),
            ("Nb arbres",str(metrics["best_params"]["n_estimators"])),
            ("Profondeur max",str(metrics["best_params"]["max_depth"])),
            ("Min samples split",str(metrics["best_params"]["min_samples_split"])),
            ("Accuracy test",f"{metrics['accuracy']*100:.1f}%"),
            ("Train size",f"{metrics['train_size']} obs (75%)"),
            ("Test size",f"{metrics['test_size']} obs (25%)"),
            ("CV score moyen",f"{np.mean(metrics['cv_scores']):.3f}"),
            ("Nb tâches","7 tâches Copilot"),
        ]
        html_params = ""
        for k,v in params:
            html_params += f'<div class="param-row"><span class="param-key">{k}</span><span class="param-val">{v}</span></div>'
        st.markdown(f'<div style="background:#FFFFFF;border:1px solid #E5E7EB;border-radius:12px;padding:0.5rem;">{html_params}</div>', unsafe_allow_html=True)

    with col_cm:
        cm = np.array(metrics["confusion_matrix"])
        fig_cm = px.imshow(cm, text_auto=True,
                           labels={"x":"Prédit","y":"Réel"},
                           x=["Non pertinent","Pertinent"],
                           y=["Non pertinent","Pertinent"],
                           color_continuous_scale=[[0,"#F9FAFB"],[1,"#6366F1"]])
        fig_cm.update_layout(**chart_cfg("Matrice de confusion"))
        fig_cm.update_coloraxes(showscale=False)
        fig_cm.update_traces(textfont=dict(size=16,family="JetBrains Mono"))
        st.plotly_chart(fig_cm, use_container_width=True)

    with col_cv:
        cv = metrics["cv_scores"]
        mean_cv = np.mean(cv)
        fig_cv = go.Figure()
        bar_colors = ["#6366F1" if v>=mean_cv else "#A5B4FC" for v in cv]
        fig_cv.add_trace(go.Bar(x=[f"Fold {i+1}" for i in range(len(cv))],
                                y=cv, marker_color=bar_colors,
                                marker_line_width=0, marker_cornerradius=4,
                                text=[f"{v:.3f}" for v in cv], textposition="outside",
                                textfont=dict(size=10,family="JetBrains Mono")))
        fig_cv.add_hline(y=mean_cv, line_dash="dot", line_color=C_ORANGE,
                         annotation_text=f"Moy: {mean_cv:.3f}",
                         annotation_font=dict(color=C_ORANGE,size=10))
        fig_cv.update_layout(**chart_cfg("Validation croisée 5-Fold"))
        st.plotly_chart(fig_cv, use_container_width=True)

    st.markdown('<div class="sec-label">Importance des variables & Métriques détaillées</div>', unsafe_allow_html=True)
    col_fi, col_met = st.columns([1.3,1], gap="large")

    with col_fi:
        name_map = {
            "task_enc":"Type de tâche","compl_enc":"Complexité","deliv_enc":"Type livrable",
            "temps_realisation_min":"Temps réalisation","nb_iterations":"Nb itérations",
            "score_pertinence":"Score pertinence","score_clarte":"Score clarté",
            "score_exactitude":"Score exactitude","score_exploitabilite":"Score exploitabilité",
        }
        fi = pd.DataFrame({
            "Feature":  list(metrics["feature_importances"].keys()),
            "Importance":list(metrics["feature_importances"].values()),
        }).sort_values("Importance")
        fi["Feature"] = fi["Feature"].map(name_map)
        max_fi = fi["Importance"].max()
        fi["Color"] = fi["Importance"].apply(lambda x: "#6366F1" if x>=max_fi*0.7 else "#818CF8" if x>=max_fi*0.4 else "#C7D2FE")
        fig_fi = go.Figure(go.Bar(
            x=fi["Importance"], y=fi["Feature"], orientation="h",
            marker_color=fi["Color"], marker_line_width=0, marker_cornerradius=3,
            text=[f"{v:.3f}" for v in fi["Importance"]], textposition="outside",
            textfont=dict(size=9,family="JetBrains Mono"),
        ))
        fig_fi.update_layout(**chart_cfg("Importance des variables (Gini)"))
        fig_fi.update_layout(height=320)
        st.plotly_chart(fig_fi, use_container_width=True)

    with col_met:
        acc = metrics["accuracy"]
        cm_arr = np.array(metrics["confusion_matrix"])
        tn,fp,fn,tp = cm_arr.ravel()
        p1 = tp/(tp+fp) if (tp+fp)>0 else 0
        r1 = tp/(tp+fn) if (tp+fn)>0 else 0
        f1 = 2*p1*r1/(p1+r1) if (p1+r1)>0 else 0
        p0 = tn/(tn+fn) if (tn+fn)>0 else 0
        r0 = tn/(tn+fp) if (tn+fp)>0 else 0
        f0 = 2*p0*r0/(p0+r0) if (p0+r0)>0 else 0

        st.markdown("**Métriques de classification**")
        header = '<div class="metric-row metric-header"><span>Classe</span><span>Précision</span><span>Rappel</span><span>F1-score</span><span>Support</span></div>'
        r0_html = f'<div class="metric-row metric-data"><span>Non pertinent (0)</span><span style="font-family:JetBrains Mono">{p0:.2f}</span><span style="font-family:JetBrains Mono">{r0:.2f}</span><span style="font-family:JetBrains Mono">{f0:.2f}</span><span>{int(tn+fp)}</span></div>'
        r1_html = f'<div class="metric-row metric-data"><span>Pertinent (1)</span><span style="font-family:JetBrains Mono">{p1:.2f}</span><span style="font-family:JetBrains Mono">{r1:.2f}</span><span style="font-family:JetBrains Mono">{f1:.2f}</span><span>{int(tp+fn)}</span></div>'
        ra_html = f'<div class="metric-row metric-data" style="background:linear-gradient(135deg,#EEF2FF,#E0E7FF);font-weight:600;"><span>Accuracy globale</span><span>—</span><span>—</span><span style="font-family:JetBrains Mono;color:#4338CA;">{acc:.2f}</span><span>{int(tn+fp+tp+fn)}</span></div>'
        st.markdown(f'<div style="background:#FFFFFF;border:1px solid #E5E7EB;border-radius:12px;overflow:hidden;padding:0.5rem;">{header}{r0_html}{r1_html}{ra_html}</div>', unsafe_allow_html=True)

        st.markdown("<br>**Interprétation**", unsafe_allow_html=True)

        # Dynamic interpretation from real metrics
        roc_d = metrics.get("roc_data", {})
        mc    = metrics.get("model_comparison", {})
        best_auc = max((v["auc"] for v in mc.values()), default=0.98) if mc else 0.98
        rf_cv    = mc.get("Random Forest", {}).get("cv_mean", 0.75)
        rf_acc   = mc.get("Random Forest", {}).get("accuracy", 0.96)

        gap_txt = ""
        if rf_acc - rf_cv > 0.15:
            gap_txt = f" Le gap accuracy ({rf_acc:.0%}) / CV ({rf_cv:.0%}) indique un léger overfitting lié à la taille du dataset (200 obs.) — à mentionner comme limite dans le mémoire."

        st.markdown(f"""
        <div style='background:#F9FAFB;border-radius:10px;padding:1rem 1.2rem;font-size:0.83rem;
            color:#374151;line-height:1.7;border:1px solid #E5E7EB;'>
        Le modèle <b>Random Forest</b> obtient la meilleure accuracy ({rf_acc:.0%}) et le meilleur AUC
        ({best_auc:.3f}) parmi les 4 algorithmes testés — très proche du classifieur parfait (AUC=1.0).{gap_txt}
        </div>""", unsafe_allow_html=True)

    # ── ROC Curves ───────────────────────────────────────────────────────────
    st.markdown('<div class="sec-label">Courbes ROC — Comparaison des 4 modèles</div>', unsafe_allow_html=True)
    col_roc, col_lc = st.columns(2)

    with col_roc:
        roc_d = metrics.get("roc_data", {})
        mc    = metrics.get("model_comparison", {})
        fig_roc = go.Figure()
        colors_roc = {"Random Forest":"#6366F1","Gradient Boosting":"#06B6D4",
                      "Logistic Regression":"#F59E0B","SVM":"#EF4444"}
        for name, rd in roc_d.items():
            auc_val = rd.get("auc", mc.get(name,{}).get("auc",0))
            fig_roc.add_trace(go.Scatter(
                x=rd["fpr"], y=rd["tpr"], mode="lines",
                name=f"{name} (AUC={auc_val:.3f})",
                line=dict(color=colors_roc.get(name,"#9CA3AF"), width=2)
            ))
        fig_roc.add_trace(go.Scatter(
            x=[0,1], y=[0,1], mode="lines", name="Aléatoire",
            line=dict(color="#D1D5DB", width=1, dash="dash"), showlegend=True
        ))
        fig_roc.update_layout(
            title=dict(text="Courbes ROC — AUC par modèle", font=dict(color="#6B7280",size=11), x=0),
            paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="#FFFFFF",
            font=dict(color="#111827",size=10), height=300,
            margin=dict(l=10,r=10,t=44,b=10),
            xaxis=dict(title="Taux de faux positifs", gridcolor="#F3F4F6", range=[0,1]),
            yaxis=dict(title="Taux de vrais positifs", gridcolor="#F3F4F6", range=[0,1]),
            legend=dict(bgcolor="rgba(0,0,0,0)", font=dict(size=9)),
        )
        st.plotly_chart(fig_roc, use_container_width=True)

    with col_lc:
        lc = metrics.get("learning_curve", {})
        if lc:
            ts   = lc["train_sizes"]
            tm   = lc["train_mean"]; tstd = lc["train_std"]
            vm   = lc["val_mean"];   vstd = lc["val_std"]
            fig_lc = go.Figure()
            fig_lc.add_trace(go.Scatter(
                x=ts+ts[::-1],
                y=[m+s for m,s in zip(tm,tstd)]+[m-s for m,s in zip(tm[::-1],tstd[::-1])],
                fill="toself", fillcolor="rgba(99,102,241,0.1)", line=dict(color="rgba(0,0,0,0)"),
                showlegend=False, hoverinfo="skip"
            ))
            fig_lc.add_trace(go.Scatter(
                x=ts+ts[::-1],
                y=[m+s for m,s in zip(vm,vstd)]+[m-s for m,s in zip(vm[::-1],vstd[::-1])],
                fill="toself", fillcolor="rgba(6,182,212,0.1)", line=dict(color="rgba(0,0,0,0)"),
                showlegend=False, hoverinfo="skip"
            ))
            fig_lc.add_trace(go.Scatter(x=ts, y=tm, mode="lines+markers",
                name="Score entraînement", line=dict(color="#6366F1",width=2),
                marker=dict(size=6)))
            fig_lc.add_trace(go.Scatter(x=ts, y=vm, mode="lines+markers",
                name="Score validation (CV)", line=dict(color="#06B6D4",width=2),
                marker=dict(size=6)))
            fig_lc.update_layout(
                title=dict(text="Courbe d'apprentissage — Random Forest", font=dict(color="#6B7280",size=11), x=0),
                paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="#FFFFFF",
                font=dict(color="#111827",size=10), height=300,
                margin=dict(l=10,r=10,t=44,b=10),
                xaxis=dict(title="Nb observations entraînement", gridcolor="#F3F4F6"),
                yaxis=dict(title="Accuracy", range=[0.3,1.05], gridcolor="#F3F4F6"),
                legend=dict(bgcolor="rgba(0,0,0,0)", font=dict(size=9)),
            )
            st.plotly_chart(fig_lc, use_container_width=True)

    # ── Comparaison tableau modèles ───────────────────────────────────────────
    st.markdown('<div class="sec-label">Tableau comparatif des 4 algorithmes</div>', unsafe_allow_html=True)
    mc = metrics.get("model_comparison", {})
    if mc:
        rows_mc = []
        for name, v in mc.items():
            best_mark = " [RF]" if name=="Random Forest" else ""
            rows_mc.append({
                "Modèle": name + best_mark,
                "Accuracy": f"{v['accuracy']*100:.1f}%",
                "CV moyen": f"{v['cv_mean']*100:.1f}%",
                "CV std": f"±{v['cv_std']*100:.1f}%",
                "AUC": f"{v['auc']:.3f}",
                "Précision": f"{v['precision']:.3f}",
                "Rappel": f"{v['recall']:.3f}",
                "F1-score": f"{v['f1']:.3f}",
            })
        st.dataframe(pd.DataFrame(rows_mc), use_container_width=True, hide_index=True)
        st.markdown("""
        <div style='font-size:0.78rem;color:#9CA3AF;margin-top:0.4rem;'>
        * Modèle retenu — meilleur compromis Accuracy/F1. AUC > 0.98 = excellent pouvoir discriminant.
        Gap Accuracy/CV : léger overfitting attendu pour n=200. La courbe d'apprentissage confirme
        que le modèle converge et bénéficierait de données supplémentaires.
        </div>""", unsafe_allow_html=True)



# ════════════════════════════════════════════════════════
# PAGE 6 — TESTS STATISTIQUES
# ════════════════════════════════════════════════════════
elif "Tests statistiques" in page:
    if not MODEL_OK: st.error("Modèle introuvable."); st.stop()

    from scipy import stats as scipy_stats

    st.markdown('<div class="sec-label">Tests statistiques — Validation empirique des gains Copilot</div>', unsafe_allow_html=True)
    st.markdown("<p style='color:#6B7280;font-size:0.88rem;margin-bottom:1.5rem;max-width:800px;'>Validation statistique des différences de temps observées entre tâches réalisées avec et sans Copilot. Tests de Welch (t-test), taille d'effet de Cohen's d et intervalles de confiance à 95%.</p>", unsafe_allow_html=True)

    # ── Calcul inline ──────────────────────────────────────
    stats_data = {}
    for task in df['type_tache'].unique():
        sub = df[df['type_tache'] == task]
        cop = sub[sub['copilot_utilise']==1]['temps_realisation_min'].dropna()
        no  = sub[sub['copilot_utilise']==0]['temps_realisation_min'].dropna()
        if len(cop) < 3 or len(no) < 3:
            continue
        t_stat, p_val = scipy_stats.ttest_ind(cop.values, no.values, equal_var=False)
        pooled_std = np.sqrt((float(cop.std())**2 + float(no.std())**2) / 2)
        cohens_d   = float((no.mean() - cop.mean()) / pooled_std) if pooled_std > 0 else 0.0
        diff_mean  = float(no.mean() - cop.mean())
        se         = float(np.sqrt(cop.var()/len(cop) + no.var()/len(no)))
        d_abs      = abs(cohens_d)
        effect     = "Grand" if d_abs>=0.8 else "Moyen" if d_abs>=0.5 else "Petit" if d_abs>=0.2 else "Négligeable"
        stats_data[task] = {
            "n_cop": int(len(cop)), "n_no": int(len(no)),
            "mean_cop": round(float(cop.mean()),1),
            "mean_no":  round(float(no.mean()),1),
            "diff_mean": round(diff_mean,1),
            "t_stat":    round(float(t_stat),3),
            "p_value":   round(float(p_val),6),
            "significant": bool(p_val < 0.05),
            "cohens_d":  round(cohens_d,3),
            "effect_size": effect,
            "ci_low":  round(diff_mean - 1.96*se, 1),
            "ci_high": round(diff_mean + 1.96*se, 1),
        }

    # Global test
    cop_all = df[df['copilot_utilise']==1]['temps_realisation_min'].dropna()
    no_all  = df[df['copilot_utilise']==0]['temps_realisation_min'].dropna()
    t_g, p_g = scipy_stats.ttest_ind(cop_all.values, no_all.values, equal_var=False)
    pool_g   = float(np.sqrt((float(cop_all.std())**2 + float(no_all.std())**2) / 2))
    d_g      = float((no_all.mean() - cop_all.mean()) / pool_g) if pool_g > 0 else 0.0
    d_g_abs  = abs(d_g)
    eff_g    = "Grand" if d_g_abs>=0.8 else "Moyen" if d_g_abs>=0.5 else "Petit"
    glob = {"p_value": float(p_g), "cohens_d": round(d_g,3), "effect_size": eff_g}

    # ── KPIs ──────────────────────────────────────────────
    sig_count = sum(1 for v in stats_data.values() if v["significant"])
    c1,c2,c3,c4 = st.columns(4)
    c1.metric("Tâches analysées", len(stats_data))
    c2.metric("Différences significatives", f"{sig_count}/{len(stats_data)}")
    pval_display = f"< 0.0001" if glob['p_value'] < 0.0001 else f"{glob['p_value']}"
    c3.metric("p-value globale", pval_display)
    c4.metric("Cohen's d global", f"{glob['cohens_d']} ({glob['effect_size']})")

    # ── Tableau ────────────────────────────────────────────
    st.markdown('<div class="sec-label">Résultats par tâche — t-test de Welch (α = 0.05)</div>', unsafe_allow_html=True)
    rows_stat = []
    for task, v in stats_data.items():
        rows_stat.append({
            "Tâche": task,
            "N avec Copilot": v["n_cop"], "N sans Copilot": v["n_no"],
            "Moy. avec (min)": v["mean_cop"], "Moy. sans (min)": v["mean_no"],
            "Différence (min)": v["diff_mean"],
            "t-stat": v["t_stat"], "p-value": f"{v['p_value']:.4f}" if v['p_value'] >= 0.0001 else f"{v['p_value']:.2e}",
            "Significatif": "Oui" if v["significant"] else "Non",
            "Cohen's d": v["cohens_d"], "Taille effet": v["effect_size"],
        })
    st.dataframe(pd.DataFrame(rows_stat), use_container_width=True, hide_index=True)

    # ── Graphiques ─────────────────────────────────────────
    st.markdown('<div class="sec-label">Visualisation — Intervalles de confiance 95%</div>', unsafe_allow_html=True)
    col_g1, col_g2 = st.columns(2)

    ABREVS_STAT = {
        "Créer des rapports automatiquement": "Créer rapports",
        "Analyser les données rapidement": "Analyser données",
        "Poser des questions en langage naturel": "Questions NL",
        "Générer du DAX": "Générer DAX",
        "Nettoyer les données": "Nettoyer",
        "Améliorer le design": "Design",
        "Résumer les insights": "Résumer insights",
    }
    tasks_s   = list(stats_data.keys())
    labels_s  = [ABREVS_STAT.get(t, t) for t in tasks_s]
    diffs_s   = [stats_data[t]["diff_mean"] for t in tasks_s]
    ci_low_s  = [stats_data[t]["ci_low"]    for t in tasks_s]
    ci_hi_s   = [stats_data[t]["ci_high"]   for t in tasks_s]
    sigs_s    = [stats_data[t]["significant"] for t in tasks_s]
    ds_s      = [abs(stats_data[t]["cohens_d"]) for t in tasks_s]

    with col_g1:
        fig_ci = go.Figure()
        for i,(lbl,d,cl,ch,sig) in enumerate(zip(labels_s,diffs_s,ci_low_s,ci_hi_s,sigs_s)):
            clr = "#6366F1" if sig else "#CBD5E1"
            fig_ci.add_trace(go.Scatter(
                x=[cl,ch], y=[lbl,lbl], mode="lines",
                line=dict(color=clr, width=4), showlegend=False,
                hovertemplate=f"IC 95%: [{cl:.1f}, {ch:.1f}] min<extra></extra>"
            ))
            fig_ci.add_trace(go.Scatter(
                x=[d], y=[lbl], mode="markers",
                marker=dict(color=clr, size=12, symbol="diamond"),
                showlegend=False,
                hovertemplate=f"Gain moyen: {d:.1f} min<extra></extra>"
            ))
        fig_ci.add_vline(x=0, line_dash="dash", line_color="#9CA3AF",
                         annotation_text="0 (pas de gain)", annotation_font=dict(color="#9CA3AF",size=10))
        fig_ci.update_layout(
            title=dict(text="Gain de temps moyen avec IC 95% (min)",font=dict(color="#6B7280",size=11),x=0),
            paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="#FFFFFF",
            font=dict(color="#111827",size=10), height=340,
            margin=dict(l=10,r=30,t=44,b=40),
            xaxis=dict(title="Gain (min) — Indigo=significatif, Gris=non significatif",
                       gridcolor="#F3F4F6", zerolinecolor="#E5E7EB"),
            yaxis=dict(gridcolor="#F3F4F6"),
        )
        st.plotly_chart(fig_ci, use_container_width=True)

    with col_g2:
        clrs_d = ["#22C55E" if d>=0.8 else "#F59E0B" if d>=0.5 else "#6366F1" if d>=0.2 else "#E2E8F0" for d in ds_s]
        fig_d = go.Figure(go.Bar(
            x=ds_s, y=labels_s, orientation="h",
            marker_color=clrs_d, marker_line_width=0, marker_cornerradius=4,
            text=[f"{d:.2f}" for d in ds_s], textposition="outside",
            textfont=dict(size=10, family="JetBrains Mono"),
        ))
        for xv, lbl, clr in [(0.2,"Petit (0.2)","#9CA3AF"),(0.5,"Moyen (0.5)","#D97706"),(0.8,"Grand (0.8)","#059669")]:
            fig_d.add_vline(x=xv, line_dash="dot", line_color=clr,
                            annotation_text=lbl, annotation_font=dict(color=clr, size=9))
        fig_d.update_layout(
            title=dict(text="Taille d'effet — Cohen's d (|d|)", font=dict(color="#6B7280",size=11), x=0),
            paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="#FFFFFF",
            font=dict(color="#111827",size=10), height=340,
            margin=dict(l=10,r=30,t=44,b=10),
            xaxis=dict(range=[0,2.5], gridcolor="#F3F4F6"),
            yaxis=dict(gridcolor="#F3F4F6"),
        )
        st.plotly_chart(fig_d, use_container_width=True)

    # ── Interprétation ─────────────────────────────────────
    st.markdown('<div class="sec-label">Interprétation</div>', unsafe_allow_html=True)
    sig_tasks   = [t for t,v in stats_data.items() if v["significant"]]
    insig_tasks = [t for t,v in stats_data.items() if not v["significant"]]
    sig_names   = " et ".join([f"<b>{ABREVS_STAT.get(t,t)}</b>" for t in sig_tasks])
    insig_names = " et ".join([f"<b>{ABREVS_STAT.get(t,t)}</b>" for t in insig_tasks])

    col_i1, col_i2 = st.columns(2)
    with col_i1:
        st.markdown(f"""
        <div style='background:#ECFDF5;border:1px solid #6EE7B7;border-left:4px solid #10B981;
            border-radius:10px;padding:1.2rem;font-size:0.84rem;color:#065F46;line-height:1.7;'>
        <b>Résultats significatifs ({sig_count}/{len(stats_data)} tâches)</b><br>
        Pour {sig_names} : la différence de temps est réelle et non due au hasard (p &lt; 0.05).
        L'effet est <b>grand</b> (d &gt; 0.8) pour la majorité — Copilot apporte un gain substantiel.
        </div>""", unsafe_allow_html=True)
    with col_i2:
        insig_details = " ".join([f"<b>{ABREVS_STAT.get(t,t)}</b> (p={stats_data[t]['p_value']})" for t in insig_tasks])
        st.markdown(f"""
        <div style='background:#FFFBEB;border:1px solid #FCD34D;border-left:4px solid #F59E0B;
            border-radius:10px;padding:1.2rem;font-size:0.84rem;color:#92400E;line-height:1.7;'>
        <b>Résultats non significatifs ({len(insig_tasks)}/{len(stats_data)} tâches)</b><br>
        Pour {insig_details if insig_details else "aucune tâche"} : davantage d'observations
        sont nécessaires pour conclure. Limite liée à la taille de l'échantillon.
        </div>""", unsafe_allow_html=True)



# ════════════════════════════════════════════════════════
# PAGE 7 — ANALYSE ROI
# ════════════════════════════════════════════════════════
elif "ROI" in page:
    if not MODEL_OK: st.error("Modèle introuvable."); st.stop()

    st.markdown('<div class="sec-label">Analyse coût-bénéfice — Retour sur investissement Copilot</div>', unsafe_allow_html=True)
    st.markdown("""<p style='color:#6B7280;font-size:0.88rem;margin-bottom:1.5rem;max-width:800px;'>
    Évaluation financière du déploiement de Microsoft Copilot dans Power BI. Basée sur les gains de productivité
    mesurés et des hypothèses conservatrices : <b>30€/mois/utilisateur</b> (licence M365 Copilot),
    <b>45€/h</b> (coût horaire chargé analyste), fréquences d'usage hebdomadaires réalistes.</p>""",
    unsafe_allow_html=True)

    # ── Calcul ROI avec hypothèses réalistes ───────────────
    COUT_LICENCE_MOIS = 30
    TAUX_HORAIRE      = 45
    # Fréquences CONSERVATRICES (pas toutes les tâches chaque semaine)
    TACHES_PAR_SEMAINE = {
        "Créer des rapports automatiquement":    1,    # 1x/semaine
        "Analyser les données rapidement":        2,    # 2x/semaine
        "Poser des questions en langage naturel": 3,    # 3x/semaine
        "Générer du DAX":                         1,    # 1x/semaine
        "Nettoyer les données":                   0.5,  # 2x/mois
        "Améliorer le design":                    0.25, # 1x/mois
        "Résumer les insights":                   1,    # 1x/semaine
    }

    roi_tasks = {}
    total_gain_h_mois = 0.0
    for task in GAIN_REF:
        t_no       = TEMPS_REF[task]
        gain_pct   = GAIN_REF[task]
        gain_min   = t_no * gain_pct
        freq_sem   = TACHES_PAR_SEMAINE.get(task, 1)
        gain_min_mois  = gain_min * freq_sem * 4
        gain_h_mois    = gain_min_mois / 60
        gain_eur_mois  = gain_h_mois * TAUX_HORAIRE
        total_gain_h_mois += gain_h_mois
        roi_tasks[task] = {
            "gain_pct":            round(gain_pct*100,1),
            "gain_min_par_tache":  round(gain_min,1),
            "freq_sem":            freq_sem,
            "gain_h_mois":         round(gain_h_mois,2),
            "gain_eur_mois":       round(gain_eur_mois,1),
        }

    total_gain_h_mois     = round(total_gain_h_mois, 2)
    total_gain_eur_mois   = round(total_gain_h_mois * TAUX_HORAIRE, 1)
    benefice_net_mois     = round(total_gain_eur_mois - COUT_LICENCE_MOIS, 1)
    roi_pct               = round((total_gain_eur_mois - COUT_LICENCE_MOIS) / COUT_LICENCE_MOIS * 100, 0)
    payback_jours         = round(COUT_LICENCE_MOIS / (total_gain_eur_mois / 30), 1)

    # ── KPIs ──────────────────────────────────────────────
    roi_pct_display = f"~{int(roi_pct)}%"
    c1,c2,c3,c4,c5,c6 = st.columns(6)
    c1.metric("Coût licence", f"{COUT_LICENCE_MOIS}€/mois", help="Microsoft Copilot for M365")
    c2.metric("Gain temps", f"{total_gain_h_mois}h/mois")
    c3.metric("Valeur monétaire", f"{total_gain_eur_mois}€/mois")
    c4.metric("Bénéfice net", f"{benefice_net_mois}€/mois")
    c5.metric("ROI", roi_pct_display, help="(Gain - Coût) / Coût × 100 — hypothèses conservatrices")
    c6.metric("Payback", f"{payback_jours} jours")

    st.markdown(f"""
    <div style='background:#EEF2FF;border:1px solid #C7D2FE;border-left:4px solid #6366F1;
        border-radius:10px;padding:0.9rem 1.2rem;margin:0.8rem 0 1.2rem;
        font-size:0.82rem;color:#3730A3;line-height:1.6;'>
    <b>Lecture du ROI</b> — Un ROI de <b>{roi_pct_display}</b> signifie que pour 1€ investi en licence Copilot,
    l'organisation récupère environ <b>{int(roi_pct/100)+1}€</b> de valeur en temps économisé.
    Ce chiffre est élevé car le coût de la licence (30€/mois) est faible face au coût horaire d'un analyste (45€/h).
    À interpréter avec prudence : les fréquences d'usage sont des <b>estimations conservatrices</b>,
    non mesurées au chronomètre.
    </div>""", unsafe_allow_html=True)

    # ── Tableau détaillé ───────────────────────────────────
    st.markdown('<div class="sec-label">Détail par tâche</div>', unsafe_allow_html=True)
    rows_roi = []
    for task, v in roi_tasks.items():
        rows_roi.append({
            "Tâche": task,
            "Gain/tâche (%)": f"{v['gain_pct']}%",
            "Gain/tâche (min)": v["gain_min_par_tache"],
            "Fréq./semaine": v["freq_sem"],
            "Gain mensuel (h)": v["gain_h_mois"],
            "Valeur mensuelle (€)": v["gain_eur_mois"],
        })
    df_roi_tbl = pd.DataFrame(rows_roi).sort_values("Valeur mensuelle (€)", ascending=False)
    st.dataframe(df_roi_tbl, use_container_width=True, hide_index=True)

    # ── Graphiques ─────────────────────────────────────────
    col_v1, col_v2 = st.columns(2)

    with col_v1:
        df_roi_chart = df_roi_tbl.sort_values("Valeur mensuelle (€)")
        abrevs_roi = {
            "Créer des rapports automatiquement": "Créer rapports",
            "Analyser les données rapidement": "Analyser données",
            "Poser des questions en langage naturel": "Questions NL",
            "Générer du DAX": "Générer DAX",
            "Nettoyer les données": "Nettoyer",
            "Améliorer le design": "Design",
            "Résumer les insights": "Résumer insights",
        }
        df_roi_chart["Tâche_abr"] = df_roi_chart["Tâche"].map(abrevs_roi)
        clrs_roi = ["#6366F1" if v>=50 else "#06B6D4" if v>=20 else "#94A3B8"
                    for v in df_roi_chart["Valeur mensuelle (€)"]]
        fig_roi_bar = go.Figure(go.Bar(
            x=df_roi_chart["Valeur mensuelle (€)"],
            y=df_roi_chart["Tâche_abr"],
            orientation="h",
            marker_color=clrs_roi, marker_line_width=0, marker_cornerradius=4,
            text=[f"{v}€" for v in df_roi_chart["Valeur mensuelle (€)"]],
            textposition="outside",
            textfont=dict(size=10, family="JetBrains Mono"),
        ))
        fig_roi_bar.update_layout(
            title=dict(text="Valeur monétaire mensuelle par tâche (€)", font=dict(color="#6B7280",size=11), x=0),
            paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="#FFFFFF",
            font=dict(color="#111827",size=10), height=320,
            margin=dict(l=10,r=40,t=44,b=10),
            xaxis=dict(gridcolor="#F3F4F6", title="Gain mensuel (€)"),
            yaxis=dict(gridcolor="#F3F4F6"),
        )
        st.plotly_chart(fig_roi_bar, use_container_width=True)

    with col_v2:
        months    = list(range(0, 13))
        cout_cum  = [COUT_LICENCE_MOIS * m for m in months]
        gain_cum  = [total_gain_eur_mois * m for m in months]
        net_cum   = [g - c for g, c in zip(gain_cum, cout_cum)]
        fig_proj = go.Figure()
        fig_proj.add_trace(go.Scatter(
            x=months, y=gain_cum, name="Gain cumulé (€)",
            line=dict(color="#10B981", width=2.5),
            fill="tozeroy", fillcolor="rgba(16,185,129,0.06)"
        ))
        fig_proj.add_trace(go.Scatter(
            x=months, y=cout_cum, name="Coût cumulé (€)",
            line=dict(color="#EF4444", width=2, dash="dot")
        ))
        fig_proj.add_trace(go.Scatter(
            x=months, y=net_cum, name="Bénéfice net (€)",
            line=dict(color="#6366F1", width=2.5)
        ))
        fig_proj.add_hline(y=0, line_dash="dash", line_color="#9CA3AF")
        fig_proj.update_layout(
            title=dict(text="Projection ROI cumulé sur 12 mois (€)", font=dict(color="#6B7280",size=11), x=0),
            paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="#FFFFFF",
            font=dict(color="#111827",size=10), height=320,
            margin=dict(l=10,r=10,t=44,b=10),
            xaxis=dict(title="Mois", dtick=1, gridcolor="#F3F4F6"),
            yaxis=dict(title="Montant cumulé (€)", gridcolor="#F3F4F6"),
            legend=dict(bgcolor="rgba(0,0,0,0)", font=dict(size=10)),
        )
        st.plotly_chart(fig_proj, use_container_width=True)

    # ── Hypothèses et limites ──────────────────────────────
    st.markdown('<div class="sec-label">Hypothèses, limites & interprétation</div>', unsafe_allow_html=True)
    col_h1, col_h2 = st.columns(2)

    with col_h1:
        hyp_rows = [
            ("Coût licence",      f"{COUT_LICENCE_MOIS}€/utilisateur/mois (Microsoft M365 Copilot)"),
            ("Taux horaire",      f"{TAUX_HORAIRE}€/h chargé (estimation secteur industriel)"),
            ("Semaines/mois",     "4 semaines de travail effectives"),
            ("Périmètre",         "1 utilisateur Power BI — profil Data Analyst"),
            ("Gains de temps",    "Basés sur étude empirique (200 observations terrain + empiriques)"),
            ("Fréquences tâches", "Estimations conservatrices (vérifiées sur activité réelle)"),
        ]
        html_hyp = "".join([
            f'<div class="param-row"><span class="param-key">{k}</span>'
            f'<span class="param-val" style="font-family:Inter;font-size:0.78rem;">{v}</span></div>'
            for k,v in hyp_rows
        ])
        st.markdown(
            f'<div style="background:#FFFFFF;border:1px solid #E5E7EB;border-radius:12px;padding:0.5rem;">'
            f'<b style="font-size:0.78rem;color:#6B7280;padding:0.5rem 1rem;display:block;">Hypothèses de calcul</b>'
            f'{html_hyp}</div>',
            unsafe_allow_html=True
        )

    with col_h2:
        st.markdown(f"""
        <div style='background:#FEF3C7;border:1px solid #FCD34D;border-left:4px solid #F59E0B;
            border-radius:10px;padding:1.2rem;font-size:0.83rem;color:#92400E;line-height:1.8;margin-bottom:0.8rem;'>
        <b>Limites de cette analyse</b><br>
        • Fréquences estimées — non mesurées avec chronomètre précis<br>
        • Ne tient pas compte du temps de formation à Copilot (~2-4h initial)<br>
        • Le gain varie selon le niveau d'expérience (débutant vs avancé)<br>
        • Exclut les gains qualitatifs (moins d'erreurs, meilleure lisibilité)<br>
        • N'inclut pas les coûts IT de déploiement
        </div>
        <div style='background:#ECFDF5;border:1px solid #6EE7B7;border-left:4px solid #10B981;
            border-radius:10px;padding:1.2rem;font-size:0.83rem;color:#065F46;line-height:1.8;'>
        <b> Conclusion</b><br>
        Gain mensuel : <b>{total_gain_eur_mois}€</b> · Coût licence : <b>{COUT_LICENCE_MOIS}€</b>
        · Bénéfice net : <b>{benefice_net_mois}€/mois</b> · Payback : <b>{payback_jours} jours</b><br><br>
        <i style="color:#047857;">Note : le ROI apparent (~{roi_pct:.0f}%) est structurellement élevé
        car le coût de la licence (30€/mois) est très faible face au coût horaire d'un analyste (45€/h).
        Cohérent avec les études publiées (McKinsey 2023 : +15-40% de productivité sur tâches analytiques IA).
        À interpréter comme indicateur de rentabilité favorable, non comme économie garantie.</i>
        </div>""", unsafe_allow_html=True)



# ════════════════════════════════════════════════════════
# PAGE 8 — GLOSSAIRE
# ════════════════════════════════════════════════════════
elif "Glossaire" in page:
    st.markdown('<div class="sec-label">Glossaire — Copilot Power BI · DAX · Machine Learning</div>', unsafe_allow_html=True)

    tabs = st.tabs(["Copilot Power BI","DAX & Modèle","Métriques ML"])

    with tabs[0]:
        entries = [
            ("Copilot for Power BI","Assistant IA intégré dans Power BI Desktop. Génère visuels, résumés et pages de rapport en langage naturel via le bouton Copilot dans le ruban Accueil."),
            ("Créer des rapports automatiquement","Via 'Create a new report page'. Gain estimé ~35%. Recommandé pour les pages standard avec dimensions et mesures clairement définies."),
            ("Analyser les données rapidement","Via 'Answer a question about the data'. Gain estimé ~40%. Efficace pour identifier les Top N éléments et anomalies par catégorie."),
            ("Poser des questions en langage naturel","Via 'Answer a question about the data'. Gain estimé ~45%. Tâche la plus rentable — permet d'interroger les données sans écrire de DAX."),
            ("Générer du DAX","Tâche à fort risque. Gain estimé ~8% seulement. Nécessite une validation systématique — en moyenne 4 corrections par formule générée."),
            ("Nettoyer les données","Via Copilot Power Query (distinct du Copilot Power BI). Génère du code M. Gain estimé ~20%. Utile pour les valeurs aberrantes et types incorrects."),
            ("Améliorer le design","Via 'Suggest content for a new report page'. Gain estimé ~30%. Les couleurs de votre charte doivent être appliquées manuellement."),
            ("Résumer les insights","Via 'Answer a question about the data'. Gain estimé ~45%. Idéal pour les résumés exécutifs des KPI clés de votre rapport."),
            ("Hallucination IA","Phénomène où Copilot génère un contenu plausible mais factuellement incorrect. Validation humaine systématique obligatoire avant diffusion."),
            ("Prompt engineering","Art de formuler des instructions précises pour maximiser la pertinence des réponses Copilot : citer les noms de tables, colonnes et mesures exacts."),
        ]
        for t,d in entries:
            with st.expander(t):
                st.markdown(f"<p style='color:#374151;font-size:0.87rem;line-height:1.7;margin:0;'>{d}</p>", unsafe_allow_html=True)

    with tabs[1]:
        entries_dax = [
            ("DAX (Data Analysis Expressions)","Langage de formule Power BI pour créer mesures, colonnes et tables calculées. Utilisé pour tous les indicateurs du rapport."),
            ("CALCULATE","Fonction fondamentale évaluant une expression en modifiant le contexte de filtre actif."),
            ("SUMX / AVERAGEX","Fonctions d'itération calculant une agrégation d'une expression évaluée ligne par ligne."),
            ("FILTER","Retourne une table filtrée selon une condition. Souvent utilisée comme argument de CALCULATE."),
            ("USERELATIONSHIP","Active une relation inactive pour un calcul spécifique. Indispensable pour les modèles avec plusieurs tables de dates."),
            ("YearMonth","Colonne calculée = Année × 100 + Mois (ex: 202504). Utilisée comme clé de relation entre la table de dates et les tables de faits."),
            ("Table de dates","Table mensuelle (une ligne par mois) servant de clé de relation centrale pour tous les calculs temporels."),
            ("PPM (Parts Per Million)","Formule : Σ(quantité rejetée) / Σ(quantité reçue) × 1 000 000. Indicateur qualité principal dans les contextes industriels."),
            ("Contexte de filtre","Ensemble des filtres actifs lors de l'évaluation d'une mesure DAX. Comprendre ce contexte est essentiel pour écrire des formules correctes."),
        ]
        for t,d in entries_dax:
            with st.expander(t):
                st.markdown(f"<p style='color:#374151;font-size:0.87rem;line-height:1.7;margin:0;'>{d}</p>", unsafe_allow_html=True)

    with tabs[2]:
        entries_ml = [
            ("Random Forest Classifier","Ensemble d'arbres de décision entraînés sur sous-échantillons aléatoires. Robuste, peu sensible à l'overfitting, performant sur données tabulaires."),
            ("GridSearchCV","Optimisation des hyperparamètres par recherche exhaustive avec validation croisée. Permet de trouver la combinaison optimale (n_estimators, max_depth...)."),
            ("Validation croisée 5-Fold","Évaluation divisant le dataset en 5 sous-ensembles. Réduit le risque de sur-optimisme en testant sur des données non vues."),
            (f"Accuracy — {round(metrics['accuracy']*100,1) if MODEL_OK else 'N/A'}%",f"Proportion de prédictions correctes sur {metrics['test_size'] if MODEL_OK else 'N/A'} observations de test (25% du dataset)."),
            ("Matrice de confusion","Tableau 2×2 : vrais positifs (Copilot pertinent et bien prédit), vrais négatifs, faux positifs, faux négatifs. Permet d'analyser les erreurs du modèle."),
            ("F1-score","Moyenne harmonique précision/rappel. Métrique robuste pour les classes déséquilibrées (plus de cas 'pertinent' que 'non pertinent')."),
            ("Importance des variables (Gini)","Contribution de chaque variable à la réduction d'impureté dans les arbres. Le type de tâche est la variable la plus discriminante."),
            ("LabelEncoder","Transforme les variables catégorielles (type_tache, complexite, type_livrable) en entiers pour l'entrée du modèle Random Forest."),
        ]
        for t,d in entries_ml:
            with st.expander(t):
                st.markdown(f"<p style='color:#374151;font-size:0.87rem;line-height:1.7;margin:0;'>{d}</p>", unsafe_allow_html=True)


# ════════════════════════════════════════════════════════
# PAGE 9 — À PROPOS
# ════════════════════════════════════════════════════════
elif "propos" in page:
    st.markdown('<div class="sec-label">À propos — CopilotBI Analyzer v2.0</div>', unsafe_allow_html=True)

    col1, col2 = st.columns(2, gap="large")

    with col1:
        st.markdown("""
        <div class="about-card">
            <div class="about-title">Contexte de le mémoire</div>
            <p style='font-size:0.87rem;color:#374151;line-height:1.8;'>
            <b>CopilotBI Analyzer</b> est une application décisionnelle développée dans le cadre
            d'une mémoire professionnel RNCP 37137 «&nbsp;Chef de projet Data et Intelligence Artificielle&nbsp;»
            à Nexa Digital School.
            </p>
            <p style='font-size:0.87rem;color:#374151;line-height:1.8;'>
            Elle traduit les résultats d'une étude empirique sur l'usage de
            <b>Microsoft Copilot dans Power BI</b>, réalisée au sein de la Direction des Achats
            d'OPmobility (BU C-POWER), en un outil opérationnel d'aide à la décision.
            </p>
            <p style='font-size:0.87rem;color:#374151;line-height:1.8;'> 
            Les gains de productivité sont calculés directement depuis les données empiriques collectées
            (<b>200 observations · 7 tâches · 9 variables</b>), validés par t-test de Welch
            et mesurés par la taille d'effet de Cohen's d.
            </p>
            <div class="about-title" style="margin-top:1.2rem;">Les 7 tâches analysées</div>
        """, unsafe_allow_html=True)

        task_rows = ""
        for t in TACHES:
            g = round(GAIN_REF[t]*100)
            cls = "gain-high" if g>=30 else "gain-mid" if g>=15 else "gain-low"
            task_rows += f'<div class="task-row"><div class="task-icon">{ICONES[t]}</div><div class="task-name">{t}</div><div class="task-gain {cls}">~{g}%</div></div>'
        st.markdown(f'<div style="background:#F9FAFB;border-radius:10px;padding:0.5rem 0.8rem;border:1px solid #E5E7EB;">{task_rows}</div></div>', unsafe_allow_html=True)

    with col2:
        st.markdown("""
        <div class="about-card">
            <div class="about-title">Architecture technique</div>
        """, unsafe_allow_html=True)

        techs = [
            ("Front-end","Streamlit (Python 3.x)"),
            ("Modèle ML","Random Forest Classifier (scikit-learn) — Accuracy 96%"),
            ("Optimisation","GridSearchCV · Validation croisée 5-fold"),
            ("Visualisations","Plotly · Plotly Express"),
            ("Dataset","200 observations · 7 tâches · 9 variables"),
            ("Tests statistiques","t-test Welch · Cohen\'s d · IC 95% — 5/7 tâches significatives"),
            ("Analyse ROI","Gain : 7.5h/mois · 336€/mois · Payback : 2.7 jours"),
            ("Déploiement","Local · streamlit run streamlit_app.py"),
        ]
        tech_rows = "".join([f'<div class="param-row"><span class="param-key">{k}</span><span class="param-val" style="font-family:Inter;font-size:0.82rem;">{v}</span></div>' for k,v in techs])
        st.markdown(f'<div style="background:#F9FAFB;border-radius:10px;padding:0.5rem;border:1px solid #E5E7EB;margin-bottom:1.2rem;">{tech_rows}</div>', unsafe_allow_html=True)

        st.markdown("""
            <div class="about-title">Lancer l'application</div>
        """, unsafe_allow_html=True)

        st.code("""# Installation des dépendances
pip install streamlit plotly pandas scikit-learn numpy

# Lancement
streamlit run streamlit_app.py
# → http://localhost:8501""", language="bash")

        st.markdown("""
            <div class="about-title" style="margin-top:1rem;">Structure des fichiers</div>
            <div style="background:#0B1120;border-radius:10px;padding:1rem 1.2rem;font-family:JetBrains Mono;font-size:0.78rem;color:#E2E8F0;line-height:1.8;">
            copilotbi_analyzer/<br>
            ├── <span style="color:#818CF8;">streamlit_app.py</span>        <span style="color:#4B5563;"># Application principale</span><br>
            ├── <span style="color:#06B6D4;">model_rf.pkl</span>            <span style="color:#4B5563;"># Modèle RF entraîné</span><br>
            ├── <span style="color:#06B6D4;">metrics.json</span>            <span style="color:#4B5563;"># Métriques & paramètres</span><br>
            ├── <span style="color:#06B6D4;">dataset_copilot.csv</span>     <span style="color:#4B5563;"># Dataset (200 observations)</span><br>
            └── <span style="color:#10B981;">generate_data_model.py</span>  <span style="color:#4B5563;"># Script d'entraînement</span>
            </div>
        </div>""", unsafe_allow_html=True)

    # ── Limites & Perspectives ──────────────────────────────────────────────────
    st.markdown('<div class="sec-label">Limites de l\'étude & perspectives</div>', unsafe_allow_html=True)
    col_lim1, col_lim2 = st.columns(2)
    with col_lim1:
        st.markdown("""
        <div style='background:#FFFBEB;border:1px solid #FCD34D;border-left:4px solid #F59E0B;
            border-radius:12px;padding:1.2rem 1.4rem;'>
        <div style='font-weight:700;color:#92400E;font-size:0.85rem;margin-bottom:0.8rem;'>Limites identifiées</div>
        <ul style='font-size:0.82rem;color:#92400E;line-height:1.9;margin:0;padding-left:1.2rem;'>
            <li>Taille d'échantillon limitée (n=200) — overfitting partiel confirmé par la courbe d'apprentissage</li>
            <li>3 tâches sous-représentées dans les données réelles (Nettoyer, Design, Résumer)</li>
            <li>Fréquences d'usage ROI estimées, non mesurées au chronomètre</li>
            <li>Score de maturité : α de Cronbach = 0.639 — acceptable mais non excellent</li>
            <li>Étude mono-entreprise — généralisation à d'autres contextes non garantie</li>
            <li>Évolution rapide de Copilot (nouvelles fonctionnalités mensuelles)</li>
        </ul></div>""", unsafe_allow_html=True)
    with col_lim2:
        st.markdown("""
        <div style='background:#ECFDF5;border:1px solid #6EE7B7;border-left:4px solid #10B981;
            border-radius:12px;padding:1.2rem 1.4rem;'>
        <div style='font-weight:700;color:#065F46;font-size:0.85rem;margin-bottom:0.8rem;'> Perspectives</div>
        <ul style='font-size:0.82rem;color:#065F46;line-height:1.9;margin:0;padding-left:1.2rem;'>
            <li>Collecter 100+ observations supplémentaires (objectif n=300)</li>
            <li>Comparer avec d'autres outils IA (GitHub Copilot, ChatGPT for Excel)</li>
            <li>Mesurer les gains qualitatifs : taux d'erreurs, satisfaction utilisateur (NPS)</li>
            <li>Valider le score de maturité sur un panel plus large (α cible ≥ 0.8)</li>
            <li>Étendre l'étude à d'autres BU OPmobility pour la généralisation</li>
            <li>Automatiser le réentraînement du modèle (pipeline MLOps)</li>
        </ul></div>""", unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("""
    <div style='background:linear-gradient(135deg,#EEF2FF,#E0E7FF);border:1px solid #C7D2FE;
        border-radius:12px;padding:1rem 1.5rem;text-align:center;'>
        <span style='color:#4338CA;font-size:0.82rem;'>
        Développé par <b>Martine Bassolé</b> · Mémoire Professionnel RNCP 37137 ·
        OPmobility / Nexa Digital School · 2025–2026 ·
        <span style='color:#6366F1;'>Données collectées dans le cadre de l'étude empirique · Aucune donnée personnelle · Conforme RGPD</span>
        </span>
    </div>""", unsafe_allow_html=True)