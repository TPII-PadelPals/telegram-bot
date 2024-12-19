from .encuesta import handle_survey_test
from .saludar import handle_greet
from .ver_fmt import handle_format

TEST_MESSAGE_HANDLERS = [{"command": "saludar", "handler": handle_greet},
                         {"command": "ver_fmt", "handler": handle_format},
                         {"command": "encuesta", "handler": handle_survey_test}]

TEST_CALLBACK_HANDLERS = []
