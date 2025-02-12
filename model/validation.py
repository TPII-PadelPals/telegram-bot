from model.language_manager import LanguageManager


class Validation:
    def __init__(self, info: list[str]):
        self.info = info


    def validate(self, language_manager: LanguageManager) -> (bool, str|None):
        pass


class ValidateSurveyPlayer(Validation):
    INFO_FOR_SET_SURVEY_TO_PLAYER = 3
    POSITION_RATING = 2
    MAX_RATING = 5
    MIN_RATING = 1


    def validate(self, language_manager: LanguageManager) -> (bool, str|None):
        if len(self.info) == self.INFO_FOR_SET_SURVEY_TO_PLAYER:
            str_rating = self.info[self.POSITION_RATING]
            if not str_rating.isdigit():
                return False, language_manager.get("MESSAGE_INVALID_VALUE")
            rating = int(str_rating)
            if rating < self.MIN_RATING or rating > self.MAX_RATING:
                return False, language_manager.get("RATING_OUT_OF_RANGE_ERROR")
            return True, None
        # insufficient number of parameters
        return False, language_manager.get("MESSAGE_HELP_SURVEY_PLAYER")


class ValidateConfigStrokes(Validation):
    EXPECTED_INFORMATION = 3
    POSITION_OF_HABILITY = 2
    SEPARATOR_OF_STROKES = ','
    POSITION_OF_STROKES = 1
    MAX_STROKE_NUMBER = 16
    MIN_STROKE_NUMBER = 1


    def validate(self, language_manager: LanguageManager) -> (bool, str|None):
        if len(self.info) == self.EXPECTED_INFORMATION:
            hability = self.info[self.POSITION_OF_HABILITY].lower()
            # caso de error en habilidad
            if not hability in language_manager.get("STROKE_HABILITY"):
                return False, language_manager.get("MESSAGE_INCORRECT_HABILITY")
            strokes_list_str = self.info[self.POSITION_OF_STROKES].split(self.SEPARATOR_OF_STROKES)
            for strokes in strokes_list_str:
                if not strokes.isdigit():
                    return False, language_manager.get("MESSAGE_INVALID_VALUE")
                if int(strokes) > self.MAX_STROKE_NUMBER or self.MIN_STROKE_NUMBER > int(strokes):
                    return False, language_manager.get("MESSAGE_INVALID_VALUE")
            return True, None
        return False, language_manager.get("MESSAGE_HELP_STROKE")