"""
Gera o relatório diário em HTML a partir da lista de ações rankeadas.
"""
import os
from datetime import datetime
from jinja2 import Environment, FileSystemLoader
from config.settings import REPORT_OUTPUT_DIR

TEMPLATE_DIR = os.path.join(os.path.dirname(__file__), "templates")


def gerar_relatorio_html(acoes_rankeadas: list) -> str:
    """
    acoes_rankeadas: lista de resultados já processados (ver main.py).
    Retorna o caminho do arquivo HTML gerado.
    """
    os.makedirs(REPORT_OUTPUT_DIR, exist_ok=True)

    env = Environment(loader=FileSystemLoader(TEMPLATE_DIR))
    template = env.get_template("report.html")

    data_geracao = datetime.now().strftime("%d/%m/%Y %H:%M")
    html = template.render(acoes=acoes_rankeadas, data_geracao=data_geracao)

    nome_arquivo = f"relatorio_{datetime.now().strftime('%Y-%m-%d')}.html"
    caminho = os.path.join(REPORT_OUTPUT_DIR, nome_arquivo)
    with open(caminho, "w", encoding="utf-8") as f:
        f.write(html)

    # Mantém sempre uma cópia como "index.html" (última versão) para o GitHub Pages
    caminho_index = os.path.join(REPORT_OUTPUT_DIR, "index.html")
    with open(caminho_index, "w", encoding="utf-8") as f:
        f.write(html)

    return caminho
