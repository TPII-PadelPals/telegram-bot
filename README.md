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
TELEGRAM_BOT_TOKEN=<YOUR_TELEGRAM_TOKEN>
SERVICE_HOST=<SERVICE_HOST>
SERVICE_PORT=<SERVICE_PORT>
LANGUAGE=<LANGUAGE>
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
