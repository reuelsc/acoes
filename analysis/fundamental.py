"""
Análise fundamentalista básica de uma ação a partir dos dados da brapi.

Calcula um score de 0 a 100 combinando indicadores clássicos de valuation
e saúde financeira. As regras aqui são um ponto de partida simples e
devem ser refinadas/calibradas junto com o usuário.
"""


def _score_faixa(valor, faixas):
    """
    Dado um valor e uma lista de tuplas (limite_superior, pontos),
    retorna os pontos correspondentes à primeira faixa em que o valor se encaixa.
    Faixas devem estar em ordem crescente de limite.
    """
    if valor is None:
        return 0
    for limite, pontos in faixas:
        if valor <= limite:
            return pontos
    return faixas[-1][1]


def analisar_fundamentos(dados_brapi: dict) -> dict:
    """
    Recebe o dicionário retornado por brapi_client.get_quote_with_fundamentals
    e devolve um resumo com os principais indicadores e um score fundamentalista.
    """
    if not dados_brapi:
        return {"score": 0, "indicadores": {}, "observacoes": ["Sem dados fundamentalistas disponíveis."]}

    stats = dados_brapi.get("defaultKeyStatistics", {}) or {}
    fin = dados_brapi.get("financialData", {}) or {}

    pl = stats.get("trailingPE") or fin.get("currentPrice", 0) / (fin.get("epsTrailingTwelveMonths") or 1) if fin else None
    roe = fin.get("returnOnEquity")
    div_liquida_ebitda = fin.get("debtToEquity")
    dividend_yield = stats.get("dividendYield")
    margem_liquida = fin.get("profitMargins")

    pontos = 0
    observacoes = []

    # P/L: quanto menor (dentro do razoável), melhor
    pontos += _score_faixa(pl, [(8, 25), (15, 20), (25, 10), (999, 0)])
    if pl and pl < 10:
        observacoes.append(f"P/L baixo ({pl:.1f}) — possível subvalorização.")

    # ROE: quanto maior, melhor
    if roe is not None:
        roe_pct = roe * 100 if roe < 1 else roe
        pontos += _score_faixa(-roe_pct, [(-25, 25), (-15, 18), (-8, 10), (999, 0)])
        if roe_pct > 15:
            observacoes.append(f"ROE forte ({roe_pct:.1f}%).")

    # Dívida/Patrimônio: quanto menor, melhor
    pontos += _score_faixa(div_liquida_ebitda, [(0.5, 20), (1.0, 12), (2.0, 5), (999, 0)])

    # Dividend yield: bônus se for atrativo
    if dividend_yield:
        dy_pct = dividend_yield * 100 if dividend_yield < 1 else dividend_yield
        pontos += _score_faixa(-dy_pct, [(-8, 15), (-5, 10), (-2, 5), (999, 0)])
        if dy_pct > 6:
            observacoes.append(f"Dividend yield atrativo ({dy_pct:.1f}%).")

    # Margem líquida
    if margem_liquida is not None:
        margem_pct = margem_liquida * 100 if margem_liquida < 1 else margem_liquida
        pontos += _score_faixa(-margem_pct, [(-20, 15), (-10, 10), (-5, 5), (999, 0)])

    score = min(100, pontos)

    return {
        "score": round(score, 1),
        "indicadores": {
            "pl": pl,
            "roe": roe,
            "divida_patrimonio": div_liquida_ebitda,
            "dividend_yield": dividend_yield,
            "margem_liquida": margem_liquida,
        },
        "observacoes": observacoes,
    }
