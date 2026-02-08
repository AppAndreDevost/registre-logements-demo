from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import pandas as pd
import io
import requests

app = FastAPI()

# Autoriser l'application mobile à accéder à l'API
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# URL du fichier Excel sur GitHub
GITHUB_RAW_URL = "https://raw.githubusercontent.com/AppAndreDevost/registre-logements-demo/main/logements.xlsx"

@app.get("/")
def home():
    return {"status": "API OK"}

@app.get("/ping")
def ping():
    return {"pong": True}

@app.get("/logements")
def get_logements():
    # Télécharger le fichier Excel depuis GitHub
    resp = requests.get(GITHUB_RAW_URL)
    resp.raise_for_status()
    data = resp.content

    # Lire le fichier Excel
    df = pd.read_excel(io.BytesIO(data))

    # Convertir chaque ligne en dictionnaire
    logements = []
    for _, row in df.iterrows():
        logements.append({
            "adresse_complete": row["Adresse complète"],
            "numero_civique": row["Numéro civique"],
            "rue": row["Rue"],
            "ville": row["Ville"],
            "code_postal": row["Code postal"],
            "type_logement": row["Type de logement"],
            "nombre_chambres": row["Nombre de chambres"],
            "cout_historique": row["Coût (historique)"],
            "taux_tal_historique": row["Taux TAL (historique)"],
        })

    return {"logements": logements}

@app.get("/test-excel")
def test_excel():
    resp = requests.get(GITHUB_RAW_URL)
    df = pd.read_excel(io.BytesIO(resp.content))
    return {"colonnes": list(df.columns)}
