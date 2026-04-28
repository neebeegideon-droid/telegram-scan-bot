import os
import asyncio
import logging
import threading
from http.server import BaseHTTPRequestHandler, HTTPServer

from telegram import Update, InlineKeyboardMarkup, InlineKeyboardButton
from telegram.ext import (
    Application,
    CommandHandler,
    MessageHandler,
    CallbackQueryHandler,
    ContextTypes,
    filters
)

# ---------------- LOGGING ---------------- #
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# ---------------- TOKEN ---------------- #
BOT_TOKEN = os.getenv("8595807606:AAFJZ9RuYyEgYqJ7x-cAqzRDvu1F_jxfpGw")

if not BOT_TOKEN:
    raise ValueError("BOT_TOKEN not found!")

# ---------------- LOADING ---------------- #
LOADING_STEPS = [
    ("Scanning.", 1.2),
    ("Scanning..", 1.2),
    ("Scanning...", 1.5),
    ("Processing request...", 1.8),
    ("Contacting servers...", 2.0),
]

FINAL_MESSAGE = "Scan complete ✅\n\nDemo completed successfully."

# ---------------- BOT HANDLERS ---------------- #

async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [InlineKeyboardButton("1", callback_data="1"),
         InlineKeyboardButton("2", callback_data="2"),
         InlineKeyboardButton("3", callback_data="3")],
        [InlineKeyboardButton("4", callback_data="4"),
         InlineKeyboardButton("5", callback_data="5"),
         InlineKeyboardButton("6", callback_data="6")],
        [InlineKeyboardButton("7", callback_data="7"),
         InlineKeyboardButton("8", callback_data="8"),
         InlineKeyboardButton("9", callback_data="9")],
        [InlineKeyboardButton("0", callback_data="0")],
        [InlineKeyboardButton("🚀 RUN SCAN", callback_data="scan")]
    ]

    await update.message.reply_text(
        "Enter a number or press scan:",
        reply_markup=InlineKeyboardMarkup(keyboard)
    )

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    msg = await update.message.reply_text("Scanning...")

    for text, delay in LOADING_STEPS:
        await asyncio.sleep(delay)
        await msg.edit_text(text)

    await asyncio.sleep(1.5)
    await msg.edit_text(FINAL_MESSAGE)

async def handle_button(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    msg = await query.edit_message_text("Scanning...")

    for text, delay in LOADING_STEPS:
        await asyncio.sleep(delay)
        await msg.edit_text(text)

    await asyncio.sleep(1.5)
    await msg.edit_text(FINAL_MESSAGE)

# ---------------- BOT RUNNER ---------------- #

def run_bot():
    app = Application.builder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start_command))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    app.add_handler(CallbackQueryHandler(handle_button))

    logger.info("Bot is running...")
    app.run_polling()

# ---------------- WEB SERVER ---------------- #

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
    # Run web server in background
    threading.Thread(target=run_web).start()

    # Run bot in main thread
    run_bot()
