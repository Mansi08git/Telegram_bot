#libraries
from typing import Final
from telegram import Update
from telegram.ext import Application, CommandHandler , MessageHandler, filters, ContextTypes, CallbackContext
from telegram import Update, KeyboardButton, ReplyKeyboardMarkup
from pymongo import MongoClient
import google.generativeai as gemini
from datetime import datetime
from dotenv import load_dotenv
load_dotenv()
import os

#API KEY
TELEGRAM_API_KEY = os.getenv('TELEGRAM_API_KEY')
BOT_USERNAME : Final ='@MansiSoni_bot'
GEMINI_API_KEY = os.getenv('GEMINI_API_KEY')
gemini.configure(api_key=GEMINI_API_KEY)

#MONGO DB CONNECTION
MONGO_URI = os.getenv('MONGO_URI')
client = MongoClient(MONGO_URI)
db = client["chatbot_db"]
user_collections = db["users"]
user_history = db["chat_history"]

#START FUNCTION
async def start(update : Update, context:ContextTypes.DEFAULT_TYPE)-> None:
    chat_id= update.message.chat_id
    first_name = update.message.chat.first_name
    username = update.message.chat.username

    if user_collections.find_one({"chat_id":chat_id}):
        await update.message.reply_text(f"Hello, Welcome back {first_name}!")
        
    else:
        user_data ={
            "chat_id" : chat_id,
            "first_name": first_name,
            "username":username 
        }
        user_collections.insert_one(user_data)
        await update.message.reply_text(f"Hello {first_name}! You have been successfully registered.")

        phone_button = [[KeyboardButton("Share Phone Number", request_contact=True)]]
        reply_markup = ReplyKeyboardMarkup(phone_button, one_time_keyboard=True, resize_keyboard=True)
        await update.message.reply_text("Tap the button below to share your phone number.", reply_markup=reply_markup)

#STORE PHONE NUMBER IN DATABASE
async def phone_number_received(update: Update, context: CallbackContext) -> None:
    if update.message.contact:
        chat_id = update.message.chat_id
        first_name = update.message.chat.first_name
        username = update.message.chat.username
        phone_number = update.message.contact.phone_number

        # Check if the user is already in the database
        existing_user = user_collections.find_one({"chat_id": chat_id})
        if existing_user:
            user_collections.update_one({"chat_id": chat_id}, {"$set": {"phone_number": phone_number}})
            await update.message.reply_text("✅ Your phone number has been updated successfully!")
        else:
            user_data = {
                "chat_id": chat_id,
                "first_name": first_name,
                "username": username,
                "phone_number": phone_number
            }
            user_collections.insert_one(user_data)
            await update.message.reply_text("✅ Registration complete! Your phone number has been saved.")


#GEMINI-POWERED-CHATBOT-FUNCTION
async def gemini_chatbot(update: Update, context: CallbackContext):
    user_message= update.message.text
    chat_id = update.message.chat_id

    generation_config = {
        "temperature": 1,
        "top_p": 0.95,
        "top_k": 40,
        "max_output_tokens": 8192,
        "response_mime_type": "text/plain",
        }
    
    model = gemini.GenerativeModel(
    model_name="gemini-1.5-flash",
    generation_config=generation_config,
    )
    chat_session = model.start_chat(history=[])
    
    response = chat_session.send_message(user_message)

    user_chat = {
        "chat_id": chat_id,
        "user_msg":user_message,
        "response":response.text,
        "timestamp":datetime.now(),
    }

    user_history.insert_one(user_chat)

    await update.message.reply_text(response.text)


if __name__ == '__main__':
    print("start")
    app = Application.builder().token(TELEGRAM_API_KEY).build()
    app.add_handler(CommandHandler('start',start))
    app.add_handler(MessageHandler(filters.CONTACT, phone_number_received))
    app.add_handler(MessageHandler(filters.TEXT,gemini_chatbot))
    print("polling")
    app.run_polling(poll_interval=3)

