from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from model.telegram_bot import TelegramBot
from model.config import Config
from dotenv import load_dotenv
import threading
import uvicorn
from typing import Any
import signal
import sys

# Define the request model for message input
class MessageRequest(BaseModel):
    chat_id: int
    message: str

# Shared event to signal shutdown
shutdown_event = threading.Event()

def create_app(bot: TelegramBot) -> FastAPI:
    app = FastAPI()

    @app.post("/message")
    async def send_message(request: MessageRequest) -> dict[str, Any]:
        try:
            bot.bot.send_message(request.chat_id, request.message)
            return {"status": "success"}
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Failed to send message: {e}")

    @app.post("/message/bulk")
    async def send_messages(request: list[MessageRequest]) -> dict[str, Any]:
        try:
            for req in request:
                bot.bot.send_message(req.chat_id, req.message)
            return {"status": "success"}
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Failed to send messages: {e}")

    return app

def start_bot(bot: TelegramBot) -> None:
    try:
        bot.start()
    except Exception as e:
        print(f"Bot error: {e}")
        shutdown_event.set()

def run_server(app: FastAPI) -> None:
    try:
        uvicorn.run(app, host="0.0.0.0", port=8888)
    except Exception as e:
        print(f"Server error: {e}")
        shutdown_event.set()

def main() -> None:
    # Load environment variables
    load_dotenv(override=True)

    # Validate required configuration
    Config.validate_envs()

    # Initialize the Telegram bot
    bot = TelegramBot()

    # Start the bot in a separate thread
    bot_thread = threading.Thread(target=start_bot, args=(bot,), daemon=True)
    bot_thread.start()

    # Create the FastAPI application
    app = create_app(bot)

    # Start the server in a separate thread
    server_thread = threading.Thread(target=run_server, args=(app,), daemon=True)
    server_thread.start()

    try:
        while not shutdown_event.is_set():
            shutdown_event.wait(1)
    except KeyboardInterrupt:
        print("Shutdown signal received.")
        shutdown_event.set()

    print("Application terminated.")

if __name__ == "__main__":
    main()