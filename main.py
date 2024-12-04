from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from model.telegram_bot import TelegramBot
from model.config import Config
from dotenv import load_dotenv
import threading
import uvicorn
from typing import Any

# Define the request model for message input
class MessageRequest(BaseModel):
    chat_id: int
    message: str

def create_app(bot: TelegramBot) -> FastAPI:
    app = FastAPI()

    @app.post("/send_message/")
    async def send_message(request: MessageRequest) -> dict[str, Any]:
        try:
            bot.bot.send_message(request.chat_id, request.message)
            return {"status": "success"}
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Failed to send message: {e}")

    return app

def start_bot(bot: TelegramBot) -> None:
    bot.start()

def main() -> None:
    # Load environment variables
    load_dotenv(override=True)

    # Validate required configuration
    Config.validate_envs()

    # Initialize the Telegram bot
    bot = TelegramBot()

    # Start the bot in a separate thread to run alongside the FastAPI server
    bot_thread = threading.Thread(target=start_bot, args=(bot,), daemon=True)
    bot_thread.start()

    # Create and run the FastAPI application
    app = create_app(bot)
    uvicorn.run(app, host="0.0.0.0", port=8888)

if __name__ == "__main__":
    main()
