"""
Motor de sugestão de estratégia de opções.

Cruza o cenário identificado pela análise fundamentalista + técnica
(tendência de alta, baixa ou lateral, e a força da convicção) com a
cadeia de opções disponível, e sugere a estratégia mais adequada.

Regras iniciais (a refinar):
- Tendência de ALTA + convicção forte  -> compra de CALL (trend-following)
- Tendência de ALTA + já possui a ação -> venda coberta (covered call)
- Tendência de BAIXA                   -> compra de PUT ou trava de baixa
- Tendência LATERAL                    -> trava (spread) para reduzir custo/risco
"""


def sugerir_estrategia(tendencia: str, score_fundamentalista: float,
                        score_tecnico: float, cadeia_opcoes: list,
                        possui_em_carteira: bool = False) -> dict:
    convicao = (score_fundamentalista + score_tecnico) / 2

    calls = [o for o in cadeia_opcoes if o["type"] == "call"]
    puts = [o for o in cadeia_opcoes if o["type"] == "put"]

    if tendencia == "alta" and possui_em_carteira:
        estrategia = "Venda coberta (covered call)"
        opcao_sugerida = min(calls, key=lambda o: abs(o["delta"] - 0.30), default=None)
        justificativa = (
            "Você já possui o ativo e a tendência é de alta moderada: "
            "vender uma call fora do dinheiro gera renda extra sobre a posição, "
            "mantendo espaço para valorização até o strike."
        )
    elif tendencia == "alta" and convicao >= 60:
        estrategia = "Compra de CALL"
        opcao_sugerida = min(calls, key=lambda o: abs(o["delta"] - 0.55), default=None)
        justificativa = (
            "Cenário fundamentalista e técnico favoráveis à alta, com boa convicção: "
            "compra de call busca capturar a valorização com risco limitado ao prêmio pago."
        )
    elif tendencia == "baixa":
        estrategia = "Compra de PUT"
        opcao_sugerida = min(puts, key=lambda o: abs(o["delta"] + 0.45), default=None)
        justificativa = (
            "Cenário técnico/fundamentalista aponta enfraquecimento do ativo: "
            "compra de put busca proteção ou ganho com a queda, risco limitado ao prêmio."
        )
    else:
        estrategia = "Trava (spread) — aguardar definição de tendência"
        opcao_sugerida = None
        justificativa = (
            "Mercado sem tendência clara. Uma trava (compra e venda de opções do "
            "mesmo tipo em strikes diferentes) reduz o custo e limita o risco enquanto "
            "o cenário não se define."
        )

    return {
        "estrategia": estrategia,
        "opcao_sugerida": opcao_sugerida,
        "convicao_score": round(convicao, 1),
        "justificativa": justificativa,
    }
