"""
Pipeline principal: coleta dados -> analisa fundamentos e técnico ->
sugere estratégia de opções -> rankeia -> gera relatório.

Uso:
    python main.py
    python main.py --tickers PETR4,VALE3,ITSA4   # roda só para tickers específicos
"""
import argparse

from config.settings import UNIVERSO_ACOES, TOP_N_ACOES
from data_collector.brapi_client import get_quote_with_fundamentals, get_historical_prices
from data_collector.options_client import get_options_chain
from analysis.fundamental import analisar_fundamentos
from analysis.technical import analisar_tecnico
from analysis.options_strategy import sugerir_estrategia
from analysis.ranking import calcular_score_final, ranquear_acoes
from report.generate_report import gerar_relatorio_html


def analisar_ticker(ticker: str) -> dict:
    print(f"Analisando {ticker}...")

    dados_brapi = get_quote_with_fundamentals(ticker)
    fundamental = analisar_fundamentos(dados_brapi)

    historico = get_historical_prices(ticker)
    tecnico = analisar_tecnico(historico)

    cadeia_opcoes = get_options_chain(ticker)
    opcoes = sugerir_estrategia(
        tendencia=tecnico["tendencia"],
        score_fundamentalista=fundamental["score"],
        score_tecnico=tecnico["score"],
        cadeia_opcoes=cadeia_opcoes,
    )

    score_final = calcular_score_final(fundamental["score"], tecnico["score"])

    return {
        "ticker": ticker,
        "score_final": score_final,
        "fundamental": fundamental,
        "tecnico": tecnico,
        "opcoes": opcoes,
    }


def rodar_pipeline(tickers: list) -> list:
    resultados = [analisar_ticker(t) for t in tickers]
    top_acoes = ranquear_acoes(resultados, TOP_N_ACOES)
    caminho_relatorio = gerar_relatorio_html(top_acoes)
    print(f"\nRelatório gerado em: {caminho_relatorio}")
    return top_acoes


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--tickers",
        type=str,
        default="",
        help="Lista de tickers separados por vírgula (ex: PETR4,VALE3). "
             "Se vazio, usa o universo padrão em config/settings.py",
    )
    args = parser.parse_args()

    lista_tickers = (
        [t.strip().upper() for t in args.tickers.split(",")]
        if args.tickers
        else UNIVERSO_ACOES
    )

    resultado = rodar_pipeline(lista_tickers)

    print("\n=== RANKING FINAL ===")
    for i, r in enumerate(resultado, start=1):
        print(f"{i}. {r['ticker']} — score {r['score_final']} — {r['opcoes']['estrategia']}")
