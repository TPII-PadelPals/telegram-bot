from .configurar_disponibilidad import handle_configure_availability
from .configurar_zona import handle_configure_zone

PLAYER_MESSAGE_HANDLERS = [{"command": "configurar_disponibilidad", "handler": handle_configure_availability},
                 {"command": "configurar_zona", "handler": handle_configure_zone}]

PLAYER_CALLBACK_HANDLERS = []