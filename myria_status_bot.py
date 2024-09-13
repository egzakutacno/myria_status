import subprocess
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes

# Global variable to store the chat ID
chat_id = None

# Function to run the 'myria-node --status' command and return its output
def get_myria_status():
    try:
        print("Running 'myria-node --status' command...")
        result = subprocess.run(["myria-node", "--status"], capture_output=True, text=True)

        # Check if the command produced any output
        if result.stdout:
            print("Command output obtained successfully.")
            return result.stdout
        else:
            print("No output from 'myria-node --status'. Command may have failed.")
            return "No status output received from 'myria-node --status'. Please check if the command is running correctly."
    except Exception as e:
        print(f"Error running command: {e}")
        return f"Error running 'myria-node --status': {e}"

# Function to handle '/status' command from Telegram
async def status(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    global chat_id
    if chat_id is None:
        await update.message.reply_text("Chat ID not set. Please restart the application and provide the chat ID.")
        return

    status_output = get_myria_status()

    try:
        await context.bot.send_message(chat_id=chat_id, text=status_output)
        print("Sent status to Telegram chat.")
    except Exception as e:
        print(f"Error sending message to Telegram: {e}")

# Main function to set up the Telegram bot
def main():
    global chat_id

    # Prompt for the chat ID
    chat_id = input("Please enter your Telegram chat ID: ").strip()
    
    # Initialize the Telegram bot
    application = Application.builder().token("6613010335:AAGDNIEHvnB1NEJYtCCWEbWU02xCFKIU6Zc").build()

    # Add a handler for the '/status' command
    application.add_handler(CommandHandler("status", status))

    # Start polling for Telegram messages
    application.run_polling()

if __name__ == '__main__':
    main()
