import handlers.user.start_backend as start_backend
import handlers.user.start as start
from .info import handle_info
from .help import handle_help

USER_MESSAGE_HANDLERS = [
    {"command": "help", "handler": handle_help},
    {"command": "info", "handler": handle_info},
    {"command": "start_backend", "handler": start_backend.handle_start},
    {"command": "start", "handler": start.handle_start},
]

USER_CALLBACK_HANDLERS = [
    {"command": "start_backend", "handler": start_backend.handle_callback_query,
        "filter_fn": start_backend.filter_fn},
    {"command": "start", "handler": start.handle_callback_query,
        "filter_fn": start.filter_fn},
]
