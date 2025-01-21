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
                return False, language_manager.get("RATING_ERROR")
            return True, None
        # insufficient number of parameters
        return False, language_manager.get("MESSAGE_HELP_SURVEY_PLAYER")