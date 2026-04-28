import os
import logging
import asyncio

from telegram import Update
from telegram.ext import (
   Application,
   CommandHandler,
   MessageHandler,
   filters,
   ContextTypes,
)

# ── Logging Setup ───────────────────────────────────────────────────────────
# Configure basic logging to see bot activity and errors in the console.
logging.basicConfig(
   format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
   level=logging.INFO,
)
logger = logging.getLogger(__name__)

# ── Constants ───────────────────────────────────────────────────────────────
# Retrieve the bot token from an environment variable.
BOT_TOKEN = os.getenv("8595807606:AAFJZ9RuYyEgYqJ7x-cAqzRDvu1F_jxfpG")

# ── Command Handlers ────────────────────────────────────────────────────────

async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
   """
   Handle the /start command.
   Sends a welcome message and asks the user to share their phone number.
   """
   welcome_text = (
       "👋 Welcome!\n\n"
       "Please send your phone number so we can begin the scan."
   )
   await update.message.reply_text(welcome_text)


# ── Message Handler ─────────────────────────────────────────────────────────

async def scan_animation(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
   """
   Handle any text message from the user.
   Runs a fake scan animation by editing a single message multiple times.
   """
   try:
       # Send the initial "Scanning..." message.
       message = await update.message.reply_text("Scanning...")

       # Define the sequence of messages for the animation.
       animation_steps = [
           "Scanning.",
           "Scanning..",
           "Scanning...",
           "Processing request...",
           "Contacting servers...",
       ]

       # Iterate through each step, editing the message and waiting briefly.
       for step in animation_steps:
           await asyncio.sleep(1.5)  # Delay between edits for visual effect.
           await message.edit_text(step)

       # Final pause before showing the result.
       await asyncio.sleep(1.5)

       # Send the final scan result.
       final_text = (
           "Scan complete ✅\n"
           "No issues found.\n"
           "(This is a demo bot)"
       )
       await message.edit_text(final_text)

   except Exception as e:
       # Log any unexpected errors and notify the user.
       logger.error(f"Error during scan animation: {e}")
       await update.message.reply_text(
           "⚠️ An error occurred while processing your request. Please try again."
       )


# ── Error Handler ───────────────────────────────────────────────────────────

async def error_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
   """
   Log errors caused by updates.
   """
   logger.error(f"Update {update} caused error {context.error}")


# ── Main Entry Point ────────────────────────────────────────────────────────

def main() -> None:
   """
   Build and run the Telegram bot using polling.
   """
   # Validate that the bot token is set.
   if not BOT_TOKEN:
       logger.error("BOT_TOKEN environment variable is not set!")
       raise SystemExit("Please set the BOT_TOKEN environment variable.")

   # Build the Application using the new v20+ builder pattern.
   application = Application.builder().token(BOT_TOKEN).build()

   # Register command handlers.
   application.add_handler(CommandHandler("start", start_command))

   # Register a message handler for text messages (excluding commands).
   application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, scan_animation))

   # Register the global error handler.
   application.add_error_handler(error_handler)

   # Start the bot and run indefinitely using polling.
   logger.info("Bot is starting...")
   application.run_polling()


if __name__ == "__main__":
   main()
    
