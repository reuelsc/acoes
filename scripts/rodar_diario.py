"""
Script disparado pelo GitHub Actions todos os dias:
1. Roda o pipeline completo (gera o relatório HTML)
2. Envia um resumo para o Telegram
"""
from main import rodar_pipeline
from config.settings import UNIVERSO_ACOES, TELEGRAM_BOT_TOKEN
from bot.telegram_bot import enviar_mensagem_sincrona


def main():
    resultado = rodar_pipeline(UNIVERSO_ACOES)

    linhas = [
        f"{i+1}. {r['ticker']} — score {r['score_final']} — {r['opcoes']['estrategia']}"
        for i, r in enumerate(resultado)
    ]
    texto = "🏆 *Ranking diário — Top 10 B3*\n\n" + "\n".join(linhas)

    if TELEGRAM_BOT_TOKEN:
        enviar_mensagem_sincrona(texto)
        print("Mensagem enviada ao Telegram.")
    else:
        print("TELEGRAM_BOT_TOKEN não configurado — pulando envio.")
        print(texto)


if __name__ == "__main__":
    main()
