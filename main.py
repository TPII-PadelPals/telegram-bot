from fastapi import FastAPI, HTTPException
from model.telegram_bot_manager import TelegramBotManager
from pydantic import BaseModel
from model.telegram_bot import TelegramBot
import threading
import uvicorn
from typing import Any, Dict, List
import logging
from core.config import settings

from utils.message_processing import MessageProcessing
from utils.message_request import MessageRequest

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)


# Shared event to signal shutdown
shutdown_event = threading.Event()

def create_app(bot_manager: TelegramBotManager) -> FastAPI:
    app = FastAPI()
    bot = bot_manager.bot

    @app.post("/messages")
    async def send_message(request: MessageRequest) -> Dict[str, Any]:
        try:
            if request.chat_id < 1000:
                return {"status": "success"}
            process_request = MessageProcessing().message_processing(bot.language_manager, request)
            logger.info(f"Sending message to chat_id {process_request['chat_id']}: {process_request['message']}")
            bot.send_message(process_request["chat_id"], process_request["message"])
            return {"status": "success"}
        except Exception as e:
            logger.error(f"Error sending single message: {e}")
            raise HTTPException(status_code=500, detail=f"Failed to send message: {e}")

    @app.post("/messages/bulk")
    async def send_messages(requests: List[MessageRequest]) -> Dict[str, Any]:
        try:
            logger.info(f"Sending {len(requests)} bulk messages")
            message_processing = MessageProcessing()
            for req in requests:
                if req.chat_id < 1000:
                    continue
                process_request = message_processing.message_processing(bot.language_manager, req)
                logger.info(f"Sending message to chat_id {process_request['chat_id']}: {process_request['message']}")
                bot.send_message(process_request["chat_id"], process_request["message"])
            return {"status": "success"}
        except Exception as e:
            logger.error(f"Error sending bulk messages: {e}")
            raise HTTPException(status_code=500, detail=f"Failed to send messages: {e}")

    return app

def start_bot(bot_manager: TelegramBotManager) -> None:
    try:
        bot_manager.start()
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
    bot_manager = TelegramBotManager()

    # Start the bot in a separate thread
    bot_thread = threading.Thread(target=start_bot, args=(bot_manager,), daemon=True)
    bot_thread.start()

    # Create the FastAPI application
    app = create_app(bot_manager)

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