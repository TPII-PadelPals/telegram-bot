from .info import handle_info
from .start import handle_start, handle_callback_query

USER_MESSAGE_HANDLERS = [{"command": "info", "handler": handle_info},
                 {"command": "start", "handler": handle_start}]

USER_CALLBACK_HANDLERS = [{"command": "start", "handler": handle_callback_query},]