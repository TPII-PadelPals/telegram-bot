from .configurar_disponibilidad import availability_callback, handle_configure_availability, filter_fn as availability_filter_fn
from .encuesta_de_jugador import handle_survey_to_player
from .matchups.ver_emparejamientos import matchups_callback, handle_matchups, filter_fn
from .configurar_golpes import (
    handle_configure_strokes,
    filter_fn as strokes_filter_fn,
    callback_handler_fn,
)
from .configurar_ubicacion import handle_address_configuration
from .ver_reservas import handle_see_reserves

PLAYER_MESSAGE_HANDLERS = [
    {"command": "configurar_disponibilidad",
        "handler": handle_configure_availability},
    {"command": "ver_emparejamientos", "handler": handle_matchups},
    {"command": "configurar_ubicacion", "handler": handle_address_configuration},
    {"command": "ver_reservas", "handler": handle_see_reserves},
    {"command": "configurar_golpes", "handler": handle_configure_strokes},
    {"command": "encuesta_jugador", "handler": handle_survey_to_player},
]

PLAYER_CALLBACK_HANDLERS = [
    {
        "command": "ver_emparejamientos",
        "handler": matchups_callback,
        "filter_fn": filter_fn,
    },
    {
        "command": "configurar_golpes",
        "handler": callback_handler_fn,
        "filter_fn": strokes_filter_fn,
    }, {
        "command": "configurar_disponibilidad",
        "handler": availability_callback,
        "filter_fn": availability_filter_fn,
    },
]
