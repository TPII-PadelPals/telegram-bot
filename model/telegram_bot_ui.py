from telebot import TeleBot, types
from typing import List, Dict

class TelegramBotUI:
    def __init__(self, bot: TeleBot):
        """
        Initialize the UI handler with a TeleBot instance
        
        Args:
            bot (TeleBot): Instance of TeleBot
        """
        self.bot = bot
        
    def create_reply_keyboard(
        self,
        buttons: List[List[str]],
        resize_keyboard: bool = True,
        one_time_keyboard: bool = False,
        selective: bool = False,
        remove_keyboard: bool = False
    ) -> types.ReplyKeyboardMarkup:
        """
        Create a reply keyboard with custom buttons
        
        Args:
            buttons (List[List[str]]): 2D list of button labels
            resize_keyboard (bool): If True, keyboard will be resized to match buttons
            one_time_keyboard (bool): If True, keyboard will hide after one use
            selective (bool): If True, keyboard will show only for selected users
            remove_keyboard (bool): If True, removes the keyboard
            
        Returns:
            types.ReplyKeyboardMarkup: Configured reply keyboard
        """
        markup = types.ReplyKeyboardMarkup(
            resize_keyboard=resize_keyboard,
            one_time_keyboard=one_time_keyboard,
            selective=selective
        )
        
        if remove_keyboard:
            markup = types.ReplyKeyboardRemove(selective=selective)
            return markup
            
        for row in buttons:
            markup.row(*[types.KeyboardButton(button) for button in row])
            
        return markup
        
    def create_inline_keyboard(
        self,
        buttons: List[Dict[str, str]],
        row_width: int = 3
    ) -> types.InlineKeyboardMarkup:
        """
        Create an inline keyboard with custom buttons
        
        Args:
            buttons (List[Dict[str, str]]): List of button configs with 'text' and 'callback_data'
            row_width (int): Number of buttons per row
            
        Returns:
            types.InlineKeyboardMarkup: Configured inline keyboard
        """
        markup = types.InlineKeyboardMarkup(row_width=row_width)
        
        for button in buttons:
            markup.add(
                types.InlineKeyboardButton(
                    text=button['text'],
                    callback_data=button.get('callback_data'),
                    url=button.get('url'),
                    switch_inline_query=button.get('switch_inline_query')
                )
            )
            
        return markup