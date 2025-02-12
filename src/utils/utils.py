import pandas as pd
import os

DATA_DIR = os.path.join(os.getcwd(), "data")
TIPOS_CSV = os.path.join(DATA_DIR, "tipos.csv")

def load_types():
    """Carrega os tipos do arquivo tipos.csv e retorna um dicionário {id: nome}."""
    if not os.path.exists(TIPOS_CSV):
        raise FileNotFoundError(f"Arquivo não encontrado: {TIPOS_CSV}")

    df = pd.read_csv(TIPOS_CSV)
    return dict(zip(df["id"], df["nome"]))
