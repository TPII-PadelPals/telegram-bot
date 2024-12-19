import unittest

from utils.survey_generator import SurveyGenerator


class TestSurveyGenerator(unittest.TestCase):
    # def setUp(self):
    #     self.empty_survey = SurveyGenerator([], [])

    def test_new_survey_whit_data(self):
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

if __name__ == '__main__':
    unittest.main()
