import logging
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
from openai import OpenAI

# ================== CONFIG ==================
OPENAI_API_KEY = "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"  # 👈 Yahan apna OpenAI key daalo
TELEGRAM_BOT_TOKEN = "8131089767:AAGCq2zeHR-sCv9moT6kHT6s-Kpwp9SgcSM"  # 👈 Yahan apna Telegram token daalo
# ============================================

# OpenAI Client
client = OpenAI(api_key=OPENAI_API_KEY)

# Enable logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
logger = logging.getLogger(__name__)

# ---------- START COMMAND ----------
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("👋 Hello! I am your AI Assistant. Ask me anything!")

# ---------- CHAT HANDLER ----------
async def chat(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_input = update.message.text

    try:
        # OpenAI API se reply
        response = client.chat.completions.create(
            model="gpt-4o-mini",   # fast & cheap model
            messages=[
                {"role": "system", "content": "You are a trading AI assistant. Give short and clear answers about trading, stocks, and market updates."},
                {"role": "user", "content": user_input}
            ]
        )
        reply = response.choices[0].message.content
        await update.message.reply_text(reply)

    except error.RateLimitError:
        await update.message.reply_text("⚠️ API quota exceeded. Please check billing or try later.")
    except Exception as e:
        logger.error(f"Error: {e}")
        await update.message.reply_text("⚠️ Currently I can't fetch data. Please try again later.")

# ---------- MAIN FUNCTION ----------
def main():
    app = Application.builder().token(TELEGRAM_BOT_TOKEN).build()

    # Commands
    app.add_handler(CommandHandler("start", start))

    # Normal chat handler
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, chat))

    # Run bot
    app.run_polling()

if __name__ == "__main__":
    main()
