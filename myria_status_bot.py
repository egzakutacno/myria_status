import os
import subprocess
import time
from pathlib import Path
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes

# Function to run the 'myria-node --status' command and store the output
def run_myria_command():
    output_folder = "/root/Myria"
    Path(output_folder).mkdir(parents=True, exist_ok=True)
    
    try:
        result = subprocess.run(["myria-node", "--status"], capture_output=True, text=True)
        with open(os.path.join(output_folder, "status.txt"), "w") as f:
            f.write(result.stdout)
    except Exception as e:
        print(f"Error running command: {e}")

# Function to handle '/status' command from Telegram
async def status(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    chat_id = update.message.chat_id
    try:
        with open("/root/Myria/status.txt", "r") as f:
            status_output = f.read()
        await context.bot.send_message(chat_id=chat_id, text=status_output)
    except Exception as e:
        await context.bot.send_message(chat_id=chat_id, text=f"Error reading status: {e}")

# Function to request Telegram chat ID on first run
def get_telegram_chat_id():
    return input("Please enter your Telegram chat ID: ")

# Main function to set up the Telegram bot
def main():
    output_folder = "/root/Myria"
    Path(output_folder).mkdir(parents=True, exist_ok=True)  # Ensure the folder exists

    # Run the command and store the output every hour
    while True:
        run_myria_command()
        time.sleep(3600)  # Sleep for one hour

if __name__ == '__main__':
    # Ensure the output directory exists before continuing
    output_folder = "/root/Myria"
    Path(output_folder).mkdir(parents=True, exist_ok=True)

    # Check if chat ID is stored or prompt for it
    chat_id_file = "/root/Myria/chat_id.txt"
    if not os.path.exists(chat_id_file):
        chat_id = get_telegram_chat_id()
        with open(chat_id_file, "w") as f:
            f.write(chat_id)
    else:
        with open(chat_id_file, "r") as f:
            chat_id = f.read().strip()

    # Set up the Telegram bot
    application = Application.builder().token("6613010335:AAGDNIEHvnB1NEJYtCCWEbWU02xCFKIU6Zc").build()
    application.add_handler(CommandHandler("status", status))

    # Start the bot and run the main function
    application.run_polling()
    main()
