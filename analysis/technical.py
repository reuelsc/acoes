"""
Análise técnica básica a partir do histórico de preços (candles diários).

Calcula médias móveis, RSI, e classifica a tendência atual do ativo
(alta / baixa / lateral), que será usada pelo motor de opções para
sugerir a estratégia mais adequada.
"""
import pandas as pd
from config.settings import MEDIA_MOVEL_CURTA, MEDIA_MOVEL_LONGA, PERIODO_RSI


def _rsi(series: pd.Series, periodo: int) -> pd.Series:
    delta = series.diff()
    ganho = delta.clip(lower=0)
    perda = -delta.clip(upper=0)
    media_ganho = ganho.rolling(periodo).mean()
    media_perda = perda.rolling(periodo).mean()
    rs = media_ganho / media_perda.replace(0, 1e-9)
    return 100 - (100 / (1 + rs))


def analisar_tecnico(historico: list) -> dict:
    """
    Recebe a lista de candles retornada por brapi_client.get_historical_prices
    e devolve indicadores técnicos + tendência classificada + score técnico (0-100).
    """
    if not historico or len(historico) < MEDIA_MOVEL_LONGA + 1:
        return {
            "score": 0,
            "tendencia": "indefinida",
            "indicadores": {},
            "observacoes": ["Histórico de preços insuficiente para análise técnica."],
        }

    df = pd.DataFrame(historico)
    df = df.rename(columns={"close": "close", "date": "date"})
    df["close"] = pd.to_numeric(df["close"], errors="coerce")
    df = df.dropna(subset=["close"]).reset_index(drop=True)

    df["mm_curta"] = df["close"].rolling(MEDIA_MOVEL_CURTA).mean()
    df["mm_longa"] = df["close"].rolling(MEDIA_MOVEL_LONGA).mean()
    df["rsi"] = _rsi(df["close"], PERIODO_RSI)

    ultimo = df.iloc[-1]
    preco_atual = ultimo["close"]
    mm_curta = ultimo["mm_curta"]
    mm_longa = ultimo["mm_longa"]
    rsi = ultimo["rsi"]

    observacoes = []
    pontos = 0

    # Tendência via cruzamento de médias
    if pd.notna(mm_curta) and pd.notna(mm_longa):
        if mm_curta > mm_longa and preco_atual > mm_curta:
            tendencia = "alta"
            pontos += 40
            observacoes.append("Preço acima das médias móveis — tendência de alta.")
        elif mm_curta < mm_longa and preco_atual < mm_curta:
            tendencia = "baixa"
            pontos += 10
            observacoes.append("Preço abaixo das médias móveis — tendência de baixa.")
        else:
            tendencia = "lateral"
            pontos += 25
            observacoes.append("Médias móveis próximas — mercado sem tendência clara.")
    else:
        tendencia = "indefinida"

    # RSI: sobrecompra/sobrevenda
    if pd.notna(rsi):
        if rsi < 30:
            observacoes.append(f"RSI em {rsi:.0f} — possível sobrevenda (oportunidade de entrada).")
            pontos += 20
        elif rsi > 70:
            observacoes.append(f"RSI em {rsi:.0f} — possível sobrecompra (atenção a correção).")
            pontos += 5
        else:
            pontos += 15

    score = min(100, pontos)

    return {
        "score": round(score, 1),
        "tendencia": tendencia,
        "indicadores": {
            "preco_atual": round(float(preco_atual), 2),
            "media_movel_curta": round(float(mm_curta), 2) if pd.notna(mm_curta) else None,
            "media_movel_longa": round(float(mm_longa), 2) if pd.notna(mm_longa) else None,
            "rsi": round(float(rsi), 1) if pd.notna(rsi) else None,
        },
        "observacoes": observacoes,
    }
