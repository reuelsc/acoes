"""
Cliente para dados de opções da B3 (Greeks, volatilidade implícita, strikes).

⚠️ AINDA NÃO CONECTADO A UMA FONTE REAL.
Por enquanto retorna dados de exemplo (mock) para permitir testar o
motor de sugestão de estratégias de ponta a ponta.

Quando decidirmos a fonte definitiva (ex: OBM - https://obm.com.br/opcoes,
ou OpLab, ou outra), substituímos apenas a implementação desta função,
mantendo o mesmo formato de retorno para não quebrar o resto do sistema.
"""


def get_options_chain(ticker: str) -> list:
    """
    Retorna a cadeia de opções disponível para um ticker.

    Formato de cada item (mock):
    {
        "symbol": "PETRJ380",
        "type": "call" | "put",
        "strike": 38.0,
        "expiration": "2026-09-19",
        "premium": 1.25,
        "delta": 0.55,
        "implied_volatility": 0.34,
    }
    """
    # TODO: substituir por chamada real à API de opções escolhida.
    print(f"[options_client] AVISO: usando dados MOCK de opções para {ticker}")
    return [
        {
            "symbol": f"{ticker[:4]}J{int(38)}",
            "type": "call",
            "strike": 38.0,
            "expiration": "2026-09-19",
            "premium": 1.25,
            "delta": 0.55,
            "implied_volatility": 0.34,
        },
        {
            "symbol": f"{ticker[:4]}V{int(36)}",
            "type": "put",
            "strike": 36.0,
            "expiration": "2026-09-19",
            "premium": 0.90,
            "delta": -0.40,
            "implied_volatility": 0.31,
        },
    ]
