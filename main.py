from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from model.telegram_bot import TelegramBot
import threading
import uvicorn
from typing import Any, Dict, List
import logging
from core.config import settings

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)


# Define the request model for message input
class MessageRequest(BaseModel):
    chat_id: int
    message: str

# Shared event to signal shutdown
shutdown_event = threading.Event()

def create_app(bot: TelegramBot) -> FastAPI:
    app = FastAPI()

    @app.post("/messages")
    async def send_message(request: MessageRequest) -> Dict[str, Any]:
        try:
            if request.chat_id < 1000:
                return {"status": "success"}
            logger.info(f"Sending message to chat_id {request.chat_id}: {request.message}")
            bot.bot.send_message(request.chat_id, request.message)
            return {"status": "success"}
        except Exception as e:
            logger.error(f"Error sending single message: {e}")
            raise HTTPException(status_code=500, detail=f"Failed to send message: {e}")

    @app.post("/messages/bulk")
    async def send_messages(requests: List[MessageRequest]) -> Dict[str, Any]:
        try:
            logger.info(f"Sending {len(requests)} bulk messages")
            for req in requests:
                if req.chat_id < 1000:
                    continue
                logger.info(f"Sending message to chat_id {req.chat_id}: {req.message}")
                bot.bot.send_message(req.chat_id, req.message)
            return {"status": "success"}
        except Exception as e:
            logger.error(f"Error sending bulk messages: {e}")
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
        uvicorn.run(app, host=settings.TELEGRAM_BOT_SERVICE_HOST, port=settings.TELEGRAM_BOT_SERVICE_PORT)
    except Exception as e:
        print(f"Server error: {e}")
        shutdown_event.set()

def main() -> None:

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