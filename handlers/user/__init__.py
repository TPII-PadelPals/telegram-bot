from .info import handle_info
from .start import handle_start, handle_callback_query
from .help import handle_help

USER_MESSAGE_HANDLERS = [{"command": "info", "handler": handle_info},
                 {"command": "start", "handler": handle_start},{"command": "help", "handler": handle_help}]

USER_CALLBACK_HANDLERS = [{"command": "start", "handler": handle_callback_query},]