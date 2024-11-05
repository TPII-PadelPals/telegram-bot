from model.telegram_bot import TelegramBot
from model.config import Config
from dotenv import load_dotenv

if __name__ == '__main__':
    load_dotenv(override=True)
    Config.validate_envs()
    
    bot = TelegramBot()
    bot.start()