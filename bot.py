import os
import asyncio
import logging

from telegram import Update, InlineKeyboardMarkup, InlineKeyboardButton
from telegram.ext import (
    Application,
    CommandHandler,
    MessageHandler,
    CallbackQueryHandler,
    ContextTypes,
    filters
)

# Load environment variables from .env file
load_dotenv()

# Enable logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# Configuration
BOT_TOKEN = os.getenv("8595807606:AAFJZ9RuYyEgYqJ7x-cAqzRDvu1F_jxfpGw")
if not BOT_TOKEN:
    raise ValueError("No BOT_TOKEN found! Please set it in your .env file.")

# Fake loading sequence with delays (in seconds)
LOADING_STEPS = [
    ("Scanning.", 1.2),
    ("Scanning..", 1.2),
    ("Scanning...", 1.5),
    ("Processing request...", 1.8),
    ("Contacting servers...", 2.0),
]

FINAL_MESSAGE = (
    "Scan complete ✅\\n\\n"
    "WHATSAPP ACCOUNT HAS BEEN SUCCESSFULLY BANNED BY MULLER MD BOT 💀🏴‍☠️🦴"
)


async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """
    Handle /start command.
    Sends welcome message with a custom keyboard for number input.
    """
    # Create a custom keyboard that looks like a phone dial pad
    keyboard = [
        [
            InlineKeyboardButton("1", callback_data="1"),
            InlineKeyboardButton("2", callback_data="2"),
            InlineKeyboardButton("3", callback_data="3"),
        ],
        [
            InlineKeyboardButton("4", callback_data="4"),
            InlineKeyboardButton("5", callback_data="5"),
            InlineKeyboardButton("6", callback_data="6"),
        ],
        [
            InlineKeyboardButton("7", callback_data="7"),
            InlineKeyboardButton("8", callback_data="8"),
            InlineKeyboardButton("9", callback_data="9"),
        ],
        [
            InlineKeyboardButton("*", callback_data="*"),
            InlineKeyboardButton("0", callback_data="0"),
            InlineKeyboardButton("#", callback_data="#"),
        ],
        [
            InlineKeyboardButton("🚀 BAN NUMBER", callback_data="ban"),
        ],
    ]
    
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    welcome_text = (
        "Welcome! 💀🏴‍☠️🦸\\n\\n"
        "Enter a phone number to get it banned.\\n"
        "Use the keyboard below or type the number directly:"
    )
    
    await update.message.reply_text(welcome_text, reply_markup=reply_markup)


async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """
    Handle any text message (assumed to be a phone number).
    Runs the fake scanning animation and final ban message.
    """
    user = update.effective_user
    phone_number = update.message.text.strip()
    
    logger.info(f"User {user.id} ({user.username}) requested ban for: {phone_number}")
    
    try:
        # Step 1: Send initial scanning message
        processing_msg = await update.message.reply_text("Scanning number...")
        
        # Step 2: Run fake loading animation
        for step_text, delay in LOADING_STEPS:
            await asyncio.sleep(delay)
            await processing_msg.edit_text(step_text)
        
        # Step 3: Final result
        await asyncio.sleep(1.5)
        await processing_msg.edit_text(FINAL_MESSAGE)
        
    except Exception as e:
        logger.error(f"Error processing request for user {user.id}: {e}")
        await update.message.reply_text(
            "❌ An error occurred while processing your request. Please try again."
        )


async def handle_button(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """
    Handle inline keyboard button presses.
    Builds a number from button presses and processes ban when 'ban' is clicked.
    """
    query = update.callback_query
    await query.answer()  # Answer the callback to remove loading state
    
    user_id = update.effective_user.id
    
    # Initialize user data if not exists
    if "phone_number" not in context.user_data:
        context.user_data["phone_number"] = ""
    
    data = query.data
    
    if data == "ban":
        # Process the ban
        phone_number = context.user_data.get("phone_number", "").strip()
        
        if not phone_number:
            await query.edit_message_text(
                "❌ No number entered! Please use the keyboard to type a number first."
            )
            return
        
        try:
            # Show scanning animation
            await query.edit_message_text("Scanning number...")
            
            for step_text, delay in LOADING_STEPS:
                await asyncio.sleep(delay)
                await query.edit_message_text(step_text)
            
            await asyncio.sleep(1.5)
            await query.edit_message_text(FINAL_MESSAGE)
            
            # Reset the number for next use
            context.user_data["phone_number"] = ""
            
        except Exception as e:
            logger.error(f"Error in button handler for user {user_id}: {e}")
            await query.edit_message_text(
                "❌ An error occurred. Please use /start to try again."
            )
    
    else:
        # Append digit to phone number
        context.user_data["phone_number"] += data
        current_number = context.user_data["phone_number"]
        
        # Rebuild keyboard with current number displayed
        keyboard = [
            [
                InlineKeyboardButton("1", callback_data="1"),
                InlineKeyboardButton("2", callback_data="2"),
                InlineKeyboardButton("3", callback_data="3"),
            ],
            [
                InlineKeyboardButton("4", callback_data="4"),
                InlineKeyboardButton("5", callback_data="5"),
                InlineKeyboardButton("6", callback_data="6"),
            ],
            [
                InlineKeyboardButton("7", callback_data="7"),
                InlineKeyboardButton("8", callback_data="8"),
                InlineKeyboardButton("9", callback_data="9"),
            ],
            [
                InlineKeyboardButton("*", callback_data="*"),
                InlineKeyboardButton("0", callback_data="0"),
                InlineKeyboardButton("#", callback_data="#"),
            ],
            [
                InlineKeyboardButton("🚀 BAN NUMBER", callback_data="ban"),
            ],
            [
                InlineKeyboardButton("🔄 Clear", callback_data="clear"),
                InlineKeyboardButton("⌫ Delete", callback_data="delete"),
            ],
        ]
        
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        await query.edit_message_text(
            f"📱 Number: `{current_number}`\\n\\nTap digits or click BAN:",
            reply_markup=reply_markup,
            parse_mode="Markdown"
        )


async def handle_clear(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Clear the current number."""
    query = update.callback_query
    await query.answer()
    context.user_data["phone_number"] = ""
    
    keyboard = [
        [
            InlineKeyboardButton("1", callback_data="1"),
            InlineKeyboardButton("2", callback_data="2"),
            InlineKeyboardButton("3", callback_data="3"),
        ],
        [
            InlineKeyboardButton("4", callback_data="4"),
            InlineKeyboardButton("5", callback_data="5"),
            InlineKeyboardButton("6", callback_data="6"),
        ],
        [
            InlineKeyboardButton("7", callback_data="7"),
            InlineKeyboardButton("8", callback_data="8"),
            InlineKeyboardButton("9", callback_data="9"),
        ],
        [
            InlineKeyboardButton("*", callback_data="*"),
            InlineKeyboardButton("0", callback_data="0"),
            InlineKeyboardButton("#", callback_data="#"),
        ],
        [
            InlineKeyboardButton("🚀 BAN NUMBER", callback_data="ban"),
        ],
    ]
    
    await query.edit_message_text(
        "📱 Number: (empty)\\n\\nTap digits or click BAN:",
        reply_markup=InlineKeyboardMarkup(keyboard)
    )


async def handle_delete(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Delete last digit."""
    query = update.callback_query
    await query.answer()
    
    if "phone_number" in context.user_data and len(context.user_data["phone_number"]) > 0:
        context.user_data["phone_number"] = context.user_data["phone_number"][:-1]
    
    current_number = context.user_data.get("phone_number", "")
    
    keyboard = [
        [
            InlineKeyboardButton("1", callback_data="1"),
            InlineKeyboardButton("2", callback_data="2"),
            InlineKeyboardButton("3", callback_data="3"),
        ],
        [
            InlineKeyboardButton("4", callback_data="4"),
            InlineKeyboardButton("5", callback_data="5"),
            InlineKeyboardButton("6", callback_data="6"),
        ],
        [
            InlineKeyboardButton("7", callback_data="7"),
            InlineKeyboardButton("8", callback_data="8"),
            InlineKeyboardButton("9", callback_data="9"),
        ],
        [
            InlineKeyboardButton("*", callback_data="*"),
            InlineKeyboardButton("0", callback_data="0"),
            InlineKeyboardButton("#", callback_data="#"),
        ],
        [
            InlineKeyboardButton("🚀 BAN NUMBER", callback_data="ban"),
        ],
        [
            InlineKeyboardButton("🔄 Clear", callback_data="clear"),
            InlineKeyboardButton("⌫ Delete", callback_data="delete"),
        ],
    ]
    
    display = current_number if current_number else "(empty)"
    
    await query.edit_message_text(
        f"📱 Number: `{display}`\\n\\nTap digits or click BAN:",
        reply_markup=InlineKeyboardMarkup(keyboard),
        parse_mode="Markdown"
    )


async def error_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """
    Global error handler to prevent bot crashes.
    Logs errors and notifies user when possible.
    """
    logger.error(f"Exception while handling an update: {context.error}")
    
    # Notify user if possible
    if update and update.effective_message:
        try:
            await update.effective_message.reply_text(
                "❌ Something went wrong. Please try again or use /start to restart."
            )
        except Exception:
            pass  # If we can't send error message, just log it


def main() -> None:
    """
    Main function to start the bot.
    """
    logger.info("Starting Muller MD Bot...")
    
    # Create application
    application = Application.builder().token(BOT_TOKEN).build()
    
    # Add handlers
    application.add_handler(CommandHandler("start", start_command))
    
    # Handle inline keyboard buttons
    application.add_handler(CallbackQueryHandler(handle_button, pattern="^[0-9*#]$"))
    application.add_handler(CallbackQueryHandler(handle_clear, pattern="^clear$"))
    application.add_handler(CallbackQueryHandler(handle_delete, pattern="^delete$"))
    application.add_handler(CallbackQueryHandler(handle_button, pattern="^ban$"))
    
    # Handle text messages
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    
    # Error handler
    application.add_error_handler(error_handler)
    
    # Run the bot until Ctrl-C is pressed
    logger.info("Bot is running! Press Ctrl+C to stop.")
    application.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == "__main__":
    main()
