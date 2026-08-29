"""
Combina o score fundamentalista e o score técnico de cada ação
em um score final, e ordena para gerar o ranking do dia.
"""

# Pesos ajustáveis: hoje 50/50, pode ser calibrado depois.
PESO_FUNDAMENTALISTA = 0.5
PESO_TECNICO = 0.5


def calcular_score_final(score_fundamentalista: float, score_tecnico: float) -> float:
    return round(
        score_fundamentalista * PESO_FUNDAMENTALISTA + score_tecnico * PESO_TECNICO, 1
    )


def ranquear_acoes(resultados: list, top_n: int) -> list:
    """
    resultados: lista de dicts, cada um contendo pelo menos:
        {"ticker": str, "score_final": float, ...}
    Retorna os top_n ordenados do maior para o menor score.
    """
    return sorted(resultados, key=lambda r: r["score_final"], reverse=True)[:top_n]
