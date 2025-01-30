# Telegram Gemini Chatbot

A simple Telegram chatbot powered by Google's Gemini API and integrated with MongoDB for user management and chat history tracking.

## Features

- User Registration: New users are welcomed and registered on first interaction.
- Phone Number Collection: The bot can request and store the user's phone number.
- Chat History: Tracks the user's chat history in MongoDB.
- Gemini-Powered Responses: The bot uses Google's Gemini API to generate responses based on the user's messages.
- Polling: The bot continuously polls for new messages from users.

## Prerequisites
Before you run the bot, make sure to have the following dependencies installed:

1. Python 3.7+
2. MongoDB instance running
3. Telegram Bot API token
4. Gemini API key

##Installation

1. Clone this repository to your local machine:
```
git clone <repository_url>
```
2.Navigate to the project directory:
```
cd <project_directory>
```

3.Install required dependencies:
```
pip install -r requirements.txt
```

4.Create a .env file in the project root directory with the following contents:

```
TELEGRAM_API_KEY=<your_telegram_api_key>
GEMINI_API_KEY=<your_gemini_api_key>
MONGO_URI=<your_mongodb_connection_string>
```

Replace <your_telegram_api_key>, <your_gemini_api_key>, and <your_mongodb_connection_string> with your actual credentials.

5.Run the bot:
```
python main.py
```

## Libraries Used

- python-telegram-bot: For handling Telegram bot functionality.
- google-generativeai: For interacting with the Gemini API.
- pymongo: For MongoDB database interaction.
- dotenv: For loading environment variables from the .env file. 

## How It Works
1.Start Command (/start):

- When a user first interacts with the bot, they are registered in the MongoDB database.
- The bot sends a prompt to the user to share their phone number via a Telegram button.

2.Phone Number Collection:

- The bot requests the user's phone number and stores it in the database if provided.
- If the user has already shared their phone number, the bot updates the entry in the database.

3.Gemini-Powered Chat:

- The bot sends any user message to the Gemini API and receives a response, which it then sends back to the user.
- User messages and chatbot responses are saved in the MongoDB database under chat_history.

## MongoDB Collections
- users: Stores user data like chat_id, first_name, username, and phone_number.
- chat_history: Stores the chat history with fields like chat_id, user_msg, response, and timestamp.
