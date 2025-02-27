from handlers.test.ui_buttons import handle_configure_ui_buttons
from handlers.test.ui_inline_buttons import filter_fn, handle_configure_ui_inline_buttons, ui_inline_buttons_callback
from .encuesta import handle_survey_test
from .saludar import handle_greet
from .ver_fmt import handle_format

TEST_MESSAGE_HANDLERS = [{"command": "saludar", "handler": handle_greet},
                         {"command": "ver_fmt", "handler": handle_format},
                         {"command": "encuesta_test", "handler": handle_survey_test},
                         {"command": "ui_buttons", "handler": handle_configure_ui_buttons},
                         {"command": "ui_inline_buttons", "handler": handle_configure_ui_inline_buttons}]

TEST_CALLBACK_HANDLERS = [{
    "command": "ui_inline_buttons",
    "handler": ui_inline_buttons_callback,
    "filter_fn": filter_fn,
},]
