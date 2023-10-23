#!/usr/bin/env python
# pylint: disable=unused-argument

import sys
import logging
import json
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import Application, CallbackQueryHandler, CommandHandler, ContextTypes
from wakeonlan import send_magic_packet


logging.basicConfig(format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO)
logging.getLogger("httpx").setLevel(logging.WARNING)
logger = logging.getLogger(__name__)

# Load the config.json file an
def loader(file_path):
    global server
    global token
    config = {}
    f = open(file_path)
    config.update(json.load(f))
    token = config["token"]
    server = config["server"]
    print(token)
    print(server)

# Define the wakey command and generate a button for each server
async def wakey(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    keyboard = []
    for node in server.keys():
        keyboard.append([InlineKeyboardButton(str(node), callback_data=str(node))])
    reply_markup = InlineKeyboardMarkup(keyboard)

    await update.message.reply_text("Please choose:", reply_markup=reply_markup)

# Define the button
async def button(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.callback_query
    await query.answer()
    await query.edit_message_text(text=f"Waking up: {query.data}")
    send_magic_packet(server[query.data])

# Define the help command
async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text("""
    Use /wakey to wake up server.
    Use /update to update server list.
                                    """)
# Define the update command
async def updater(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    loader(server_file)
    await update.message.reply_text("Server list has been updated. Try /wakey again.")


def main() -> None:
    server_file = str(sys.argv[1])
    loader(server_file)
    application = Application.builder().token(token).build()
    application.add_handler(CommandHandler("wakey", wakey))
    application.add_handler(CallbackQueryHandler(button))
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(CommandHandler("update", updater))
    application.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == "__main__":
    main()
