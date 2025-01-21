import unittest
from unittest.mock import MagicMock

from model.player_survey.survey_generator import SurveyGenerator


class TestSurveyGenerator(unittest.TestCase):
    def setUp(self):
        self.empty_survey = SurveyGenerator([], [])
        self.bot = MagicMock()
        self.bot.send_poll = unittest.mock.create_autospec(
            lambda
                chat_id,
                question,
                options,
                allows_multiple_answers,
                is_anonymous: None, return_value=None)

    def test_new_survey_with_data(self):
        try:
            SurveyGenerator(["quest 1"], [["answer 1", "answer 2"]])
        except ValueError:
            raise AssertionError

    def test_more_question_than_answers(self):
        try:
            SurveyGenerator(["quest 1", "quest 2"], [["answer 1", "answer 2"]])
            raise AssertionError
        except ValueError:
            assert True
        except Exception:
            raise AssertionError

    def test_more_answers_than_question(self):
        try:
            SurveyGenerator(["quest 1"], [["answer 1", "answer 2"], ["answer 1", "answer 2"]])
            raise AssertionError
        except ValueError:
            assert True
        except Exception:
            raise AssertionError

    def test_no_answers(self):
        try:
            SurveyGenerator(["quest 1"], [[]])
            raise AssertionError
        except ValueError:
            assert True
        except Exception:
            raise AssertionError

    def test_one_answer(self):
        try:
            SurveyGenerator(["quest 1"], [["answer 1"]])
            raise AssertionError
        except ValueError:
            assert True
        except Exception:
            raise AssertionError

    def test_send_empty_survey(self):
        try:
            self.empty_survey.send_survey("", "123456")
        except Exception:
            raise AssertionError

    def test_send_one_survey(self):
        self.empty_survey.add_question("HOLA", ["MUNDO", "PLANTA"])
        self.empty_survey.send_survey(self.bot, "123456")
        self.bot.send_poll.assert_called_once_with(
            "123456",
            "HOLA",
            ["MUNDO", "PLANTA"],
            False,
            False
        )

    def test_send_one_survey_and_add_answer(self):
        self.empty_survey.add_question("HOLA", ["MUNDO", "PLANTA"])
        self.empty_survey.add_answers("HOLA", "GENTE")
        self.empty_survey.send_survey(self.bot, "123456", True)
        self.bot.send_poll.assert_called_once_with(
            "123456",
            "HOLA",
            ["MUNDO", "PLANTA", "GENTE"],
            True,
            False
        )

if __name__ == '__main__':
    unittest.main()
