# Telegram Bot

## Project Overview

This project is a Telegram bot designed to interact with users and provide various functionalities. It is built using Python and leverages the Telegram Bot API.

## Install Dependencies

To install the dependencies, run:

```
pip install -r requirements.txt
```

## Set Environment Variables

Before running the program, you need to set some environment variables in a `.env` file with the following variables:

```
GATEWAY_HOST=<GATEWAY_HOST>
GATEWAY_PORT=<GATEWAY_PORT>

TELEGRAM_BOT_SERVICE_HOST=<TELEGRAM_BOT_SERVICE_HOST>
TELEGRAM_BOT_SERVICE_PORT=<TELEGRAM_BOT_SERVICE_PORT>
TELEGRAM_BOT_TOKEN=<YOUR_TELEGRAM_TOKEN>
TELEGRAM_BOT_LANGUAGE=<TELEGRAM_BOT_LANGUAGE>

PLAYERS_SERVICE_HOST=<PLAYERS_SERVICE_HOST>
PLAYERS_SERVICE_PORT=<PLAYERS_SERVICE_PORT>
PLAYERS_SERVICE_API_KEY=<PLAYERS_SERVICE_API_KEY>

USERS_SERVICE_HOST=<USERS_SERVICE_HOST>
USERS_SERVICE_PORT=<USERS_SERVICE_PORT>
USERS_SERVICE_API_KEY=<USERS_SERVICE_API_KEY>
```

## Run the Bot

To run the bot, execute:

```
python main.py
```

## Create Your Own Bot for Local Testing

1. Create a new bot using the "BotFather" bot on Telegram.

   a. Start the bot creation process with the command `/newbot`.

   b. Give your bot a name, for example: `padelpals-<your_name>-test`.

   c. Assign a username to your bot, for example: `padelpals_<your_name>_bot`.

2. Once created, use the provided token in your Python program and set the environment variable `TELEGRAM_BOT_TOKEN` with the generated value.

## Testing Bot Functions

A mock is used for the messages received by our bot's methods, and the results obtained are verified.
