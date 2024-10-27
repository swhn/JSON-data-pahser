import json
import os
from datetime import datetime
from telegram import Update, InputFile
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes

# Load JSON data from the data/data.json file
data_path = "data/data.json"
with open(data_path, "r") as f:
    devices = json.load(f)

API_TOKEN = 'YOUR_BOT_API_TOKEN'

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Send a greeting when the /start command is issued."""
    await update.message.reply_text("Hello! Welcome to GMA Equipment warranty status bot. Send me your device's serial number (SN), and I'll show you the device details.")

def find_device(sn):
    """Helper function to search for a device by serial number."""
    for device in devices:
        if device['sn'] == sn:
            return device
    return None

def get_warranty_status(warranty_date_str):
    """Determine warranty status based on the current date."""
    # Convert ewarrantyDate from string to datetime object
    warranty_date = datetime.strptime(warranty_date_str, "%d-%m-%Y")
    current_date = datetime.now()
    
    # Check if the warranty is still valid
    if current_date <= warranty_date:
        return "Warranty In ✅", "green"  # Use green for active warranty
    else:
        return "Warranty Out ❌", "red"  # Use red for expired warranty

async def handle_sn(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle user messages with serial numbers."""
    sn = update.message.text.strip()
    device = find_device(sn)
    
    if device:
        # Determine warranty status
        warranty_status, color = get_warranty_status(device['ewarrantyDate'])
        
        # Format the device details
        details = (
            f"**Device Type**: {device['etype']}\n"
            f"**Brand**: {device['ebrand']}\n"
            f"**Model**: {device['emodel']}\n"
            f"**Install Date**: {device['einstallDate']}\n"
            f"**Warranty Date**: {device['ewarrantyDate']}\n"
            f"**Warranty Status**: <b><font color='{color}'>{warranty_status}</font></b>\n"
            f"**Customer**: {device['customer']}\n"
            f"**Location**: {device['location']}"
        )
        
        # Send the details message
        await update.message.reply_text(details, parse_mode="HTML")

        # Send the image from the images/ directory
        image_path = os.path.join("images", device['image'])
        try:
            with open(image_path, 'rb') as img:
                await update.message.reply_photo(photo=InputFile(img))
        except FileNotFoundError:
            await update.message.reply_text("Image not found.")
    else:
        await update.message.reply_text("No device found with that serial number.")

def main():
    # Create an application instance with your bot token
    app = ApplicationBuilder().token(API_TOKEN).build()

    # Register the command handler for /start
    app.add_handler(CommandHandler("start", start))

    # Register a handler for SN search
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_sn))

    # Start polling for updates
    print("Bot is running...")
    app.run_polling()

if __name__ == '__main__':
    main()
