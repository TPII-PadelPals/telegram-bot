from .configurar_disponibilidad import handle_configure_availability
from .configurar_zona import handle_configure_zone
from .ver_emparejamientos import handle_see_matches
from .configurar_ubicacion import handle_configure_location
from .configurar_golpes import handle_configure_strokes
from .ver_reservas import handle_see_reserves
from .responder_al_emparejamiento import handle_respond_to_matchmaking_accept, handle_respond_to_matchmaking_reject

PLAYER_MESSAGE_HANDLERS = [{"command": "configurar_disponibilidad",
                            "handler": handle_configure_availability},
                           {"command": "configurar_zona",
                            "handler": handle_configure_zone},
                           {"command": "ver_emparejamientos",
                            "handler": handle_see_matches},
                           {"command": "configurar_ubicacion",
                            "handler": handle_configure_location},
                           {"command": "ver_reservas",
                            "handler": handle_see_reserves},
                           {"command": "aceptar_emparejamiento",
                            "handler": handle_respond_to_matchmaking_accept},
                           {"command": "rechazar_emparejamiento",
                            "handler": handle_respond_to_matchmaking_reject},
                           {"command": "configurar_golpes",
                            "handler": handle_configure_strokes}]

PLAYER_CALLBACK_HANDLERS = []
