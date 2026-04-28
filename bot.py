import os
import asyncio
import logging
import threading
from http.server import BaseHTTPRequestHandler, HTTPServer

from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes

# ---------------- TOKEN ---------------- #
BOT_TOKEN = os.getenv("8595807606:AAFJZ9RuYyEgYqJ7x-cAqzRDvu1F_jxfpGw")

if not BOT_TOKEN:
    raise ValueError("BOT_TOKEN not found!")

# ---------------- LOGGING ---------------- #
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# ---------------- BOT ---------------- #
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    msg = await update.message.reply_text("Scanning...")

    steps = ["Scanning.", "Scanning..", "Scanning...", "Processing...", "Done ✅"]

    for step in steps:
        await asyncio.sleep(1.5)
        await msg.edit_text(step)

# ---------------- RUN BOT ---------------- #
def run_bot():
    app = Application.builder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))

    logger.info("Bot is running...")
    app.run_polling()

# ---------------- WEB (FOR RENDER) ---------------- #
class Handler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.end_headers()
        self.wfile.write(b'Bot is running')

def run_web():
    port = int(os.environ.get("PORT", 10000))
    server = HTTPServer(("0.0.0.0", port), Handler)
    server.serve_forever()

# ---------------- START ---------------- #
if __name__ == "__main__":
    threading.Thread(target=run_web).start()
    run_bot()
