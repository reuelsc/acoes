"""
Cliente para a API brapi.dev — cotações, histórico de preços e
indicadores fundamentalistas das ações da B3.

Docs: https://brapi.dev/docs
Sandbox sem token: PETR4, VALE3, MGLU3, ITUB4
"""
import requests
from config.settings import BRAPI_TOKEN

BASE_URL = "https://brapi.dev/api"


def _headers():
    if BRAPI_TOKEN:
        return {"Authorization": f"Bearer {BRAPI_TOKEN}"}
    return {}


def get_quote_with_fundamentals(ticker: str) -> dict:
    """
    Busca cotação atual + indicadores fundamentalistas de um ticker.
    Retorna um dicionário com os dados brutos da API, ou None em caso de erro.
    """
    params = {
        "modules": "defaultKeyStatistics,financialData,summaryProfile",
        "dividends": "true",
    }
    url = f"{BASE_URL}/quote/{ticker}"
    try:
        resp = requests.get(url, headers=_headers(), params=params, timeout=15)
        resp.raise_for_status()
        data = resp.json()
        results = data.get("results", [])
        return results[0] if results else None
    except requests.RequestException as e:
        print(f"[brapi_client] Erro ao buscar {ticker}: {e}")
        return None


def get_historical_prices(ticker: str, range_: str = "6mo", interval: str = "1d") -> list:
    """
    Busca histórico de preços (OHLCV) para cálculo de indicadores técnicos.
    range_: '1mo', '3mo', '6mo', '1y', '2y', '5y', 'max'
    interval: '1d', '1wk', '1mo'
    Retorna lista de candles (dict) em ordem cronológica.
    """
    params = {"range": range_, "interval": interval}
    url = f"{BASE_URL}/quote/{ticker}"
    try:
        resp = requests.get(url, headers=_headers(), params=params, timeout=15)
        resp.raise_for_status()
        data = resp.json()
        results = data.get("results", [])
        if not results:
            return []
        return results[0].get("historicalDataPrice", [])
    except requests.RequestException as e:
        print(f"[brapi_client] Erro ao buscar histórico de {ticker}: {e}")
        return []


def list_available_tickers(search: str = "", type_: str = "stock") -> list:
    """
    Lista/filtra tickers disponíveis na B3 (para a busca sob demanda do
    dashboard/bot, permitindo autocompletar ou validar um código digitado).
    """
    params = {"type": type_}
    if search:
        params["search"] = search
    url = f"{BASE_URL}/v2/tickers"
    try:
        resp = requests.get(url, headers=_headers(), params=params, timeout=15)
        resp.raise_for_status()
        return resp.json().get("stocks", [])
    except requests.RequestException as e:
        print(f"[brapi_client] Erro ao listar tickers: {e}")
        return []
