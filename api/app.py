"""
Backend FastAPI — serve:
1. O relatório diário (últimas 10 melhores ações)
2. Busca sob demanda de qualquer ticker (usado pelo dashboard e pelo bot)

Rodar localmente:
    uvicorn api.app:app --reload

Deploy sugerido: Render (free tier) ou Railway.
"""
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware

from main import analisar_ticker, rodar_pipeline
from config.settings import UNIVERSO_ACOES

app = FastAPI(title="Análise de Ações B3 - API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # ajustar para o domínio do dashboard em produção
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def raiz():
    return {"status": "ok", "mensagem": "API de Análise de Ações B3"}


@app.get("/ranking")
def ranking_diario():
    """Retorna o ranking das melhores ações (usa o universo padrão)."""
    resultado = rodar_pipeline(UNIVERSO_ACOES)
    return {"acoes": resultado}


@app.get("/analisar/{ticker}")
def analisar(ticker: str):
    """Busca sob demanda: análise completa de um ticker específico."""
    ticker = ticker.upper().strip()
    if not ticker.isalnum():
        raise HTTPException(status_code=400, detail="Ticker inválido.")

    resultado = analisar_ticker(ticker)
    if not resultado["fundamental"]["indicadores"] and not resultado["tecnico"]["indicadores"]:
        raise HTTPException(status_code=404, detail=f"Não foi possível encontrar dados para {ticker}.")
    return resultado
