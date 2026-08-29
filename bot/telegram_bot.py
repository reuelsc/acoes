"""
Bot do Telegram:
- Comando /analisar TICKER -> roda a análise na hora e responde
- Comando /ranking -> mostra as 10 melhores ações do último relatório
- Envio automático do relatório diário (chamado pelo GitHub Actions)

Configuração:
1. Crie um bot via @BotFather no Telegram e copie o token.
2. Preencha TELEGRAM_BOT_TOKEN e TELEGRAM_CHAT_ID no .env
3. Rode: python bot/telegram_bot.py   (para o bot ficar ouvindo comandos)

⚠️ Para o bot responder comandos a qualquer hora, ele precisa ficar
rodando continuamente — sugerido hospedar no Render (free tier, web service
"worker") junto com a API, ou usar webhook em vez de polling.
"""
import asyncio
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes

from config.settings import TELEGRAM_BOT_TOKEN, TELEGRAM_CHAT_ID
from main import analisar_ticker, rodar_pipeline
from config.settings import UNIVERSO_ACOES


async def cmd_start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Olá! Comandos disponíveis:\n"
        "/analisar TICKER — ex: /analisar PETR4\n"
        "/ranking — top 10 ações do dia"
    )


async def cmd_analisar(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.args:
        await update.message.reply_text("Use assim: /analisar PETR4")
        return

    ticker = context.args[0].upper().strip()
    await update.message.reply_text(f"Analisando {ticker}... ⏳")

    resultado = analisar_ticker(ticker)
    f = resultado["fundamental"]
    t = resultado["tecnico"]
    o = resultado["opcoes"]

    texto = (
        f"📊 *{ticker}* — score final {resultado['score_final']}\n\n"
        f"*Fundamentalista* ({f['score']}): {' '.join(f['observacoes']) or 'sem observações'}\n\n"
        f"*Técnico* ({t['score']} — {t['tendencia']}): {' '.join(t['observacoes']) or 'sem observações'}\n\n"
        f"*Opções — {o['estrategia']}*: {o['justificativa']}"
    )
    await update.message.reply_text(texto, parse_mode="Markdown")


async def cmd_ranking(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Calculando ranking do dia... ⏳ (pode levar um minuto)")
    resultado = rodar_pipeline(UNIVERSO_ACOES)
    linhas = [
        f"{i+1}. {r['ticker']} — {r['score_final']} — {r['opcoes']['estrategia']}"
        for i, r in enumerate(resultado)
    ]
    await update.message.reply_text("🏆 *Top 10 do dia*\n" + "\n".join(linhas), parse_mode="Markdown")


def enviar_mensagem_sincrona(texto: str):
    """Usado pelo GitHub Actions para enviar o relatório diário sem manter o bot rodando."""
    from telegram import Bot
    bot = Bot(token=TELEGRAM_BOT_TOKEN)
    asyncio.run(bot.send_message(chat_id=TELEGRAM_CHAT_ID, text=texto, parse_mode="Markdown"))


def main():
    app = Application.builder().token(TELEGRAM_BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", cmd_start))
    app.add_handler(CommandHandler("analisar", cmd_analisar))
    app.add_handler(CommandHandler("ranking", cmd_ranking))
    print("Bot rodando... (Ctrl+C para parar)")
    app.run_polling()


if __name__ == "__main__":
    main()
