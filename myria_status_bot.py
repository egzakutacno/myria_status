import subprocess
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes
import os

# File path to store the chat ID
CHAT_ID_FILE = '/root/myria_chat_id.txt'

def get_chat_id():
    """
    Retrieve the stored chat ID or prompt the user for it if not already stored.
    """
    if os.path.exists(CHAT_ID_FILE):
        with open(CHAT_ID_FILE, 'r') as file:
            return file.read().strip()  # Read and return the stored chat ID
    else:
        chat_id = input("Please enter your Telegram chat ID: ")  # Prompt for chat ID if not stored
        with open(CHAT_ID_FILE, 'w') as file:
            file.write(chat_id)  # Store the chat ID in a file for future use
        return chat_id

def get_myria_status():
    """
    Execute the 'myria-node --status' command and return its output.
    """
    try:
        print("Running 'myria-node --status' command...")
        result = subprocess.run(["myria-node", "--status"], capture_output=True, text=True)
        if result.stdout:
            return result.stdout  # Return the command output if successful
        else:
            return "No status output received from 'myria-node --status'. Please check if the command is running correctly."
    except Exception as e:
        return f"Error running 'myria-node --status': {e}"

async def status(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """
    Handler for the '/status' command sent from Telegram.
    """
    chat_id = get_chat_id()  # Get the stored or newly entered chat ID
    status_output = get_myria_status()
    
    try:
        await context.bot.send_message(chat_id=chat_id, text=status_output)
        print("Sent status to Telegram chat.")
    except Exception as e:
        print(f"Error sending message to Telegram: {e}")

def main():
    """
    Main function to initialize the Telegram bot and start polling for messages.
    """
    # Initialize the Telegram bot with the provided token
    application = Application.builder().token("6613010335:AAGDNIEHvnB1NEJYtCCWEbWU02xCFKIU6Zc").build()

    # Add a handler for the '/status' command
    application.add_handler(CommandHandler("status", status))

    # Start polling for Telegram messages
    application.run_polling()

if __name__ == '__main__':
    main()
