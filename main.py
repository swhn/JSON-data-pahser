import json
import os
from datetime import datetime
from telegram import Update, InputFile
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes

# Load JSON data from the data/data.json file
data_path = "data/data.json"
with open(data_path, "r") as f:
    devices = json.load(f)

# Access the API token from the secrets
API_TOKEN = os.environ['API_TOKEN']

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Hello! Send me a serial number (SN), and I'll show you the device details and image.")

def find_device(sn):
    for device in devices:
        if device['sn'] == sn:
            return device
    return None

def get_warranty_status(warranty_date_str):
    warranty_date = datetime.strptime(warranty_date_str, "%d-%m-%Y")
    current_date = datetime.now()
    if current_date <= warranty_date:
        return "Warranty In ✅", "green"
    else:
        return "Warranty Out ❌", "red"

async def handle_sn(update: Update, context: ContextTypes.DEFAULT_TYPE):
    sn = update.message.text.strip()
    device = find_device(sn)
    
    if device:
        warranty_status, color = get_warranty_status(device['ewarrantyDate'])
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
        await update.message.reply_text(details, parse_mode="HTML")

        # Send the image
        image_path = os.path.join("images", device['image'])
        try:
            with open(image_path, 'rb') as img:
                await update.message.reply_photo(photo=InputFile(img))
        except FileNotFoundError:
            await update.message.reply_text("Image not found.")
    else:
        await update.message.reply_text("No device found with that serial number.")

def main():
    app = ApplicationBuilder().token(API_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_sn))
    print("Bot is running...")
    app.run_polling()

if __name__ == '__main__':
    main()
