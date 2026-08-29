"""
Configurações gerais do sistema.
"""
import os
from dotenv import load_dotenv

load_dotenv()

# --- Chaves de API ---
BRAPI_TOKEN = os.getenv("BRAPI_TOKEN", "")
OPTIONS_API_TOKEN = os.getenv("OPTIONS_API_TOKEN", "")
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN", "")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID", "")

# --- Universo de ações analisadas na rodada diária ---
# Lista inicial de exemplo (ações de maior liquidez do Ibovespa).
# Ajuste livremente - o pipeline vai calcular o score de cada uma
# e selecionar as 10 melhores para o relatório.
UNIVERSO_ACOES = [
    "PETR4", "VALE3", "ITUB4", "BBDC4", "ABEV3",
    "B3SA3", "WEGE3", "MGLU3", "RENT3", "SUZB3",
    "GGBR4", "ITSA4", "BBAS3", "PRIO3", "EQTL3",
]

# Quantas ações finais entram no relatório diário
TOP_N_ACOES = 10

# --- Parâmetros de análise técnica ---
MEDIA_MOVEL_CURTA = 9
MEDIA_MOVEL_LONGA = 21
PERIODO_RSI = 14

# --- Caminhos de saída ---
REPORT_OUTPUT_DIR = "report/output"
