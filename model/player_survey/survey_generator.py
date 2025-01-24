class SurveyGenerator:
    MINIMAL_ANSWER_FOR_QUESTION = 2

    def __init__(self, questions: list[str], answers: list[list[str]]):
        # verificacion de datos
        if len(questions) != len(answers):
            raise ValueError("Questions and answers must have same length.")
        for answer in answers:
            if len(answer) < self.MINIMAL_ANSWER_FOR_QUESTION:
                raise ValueError("The answer must have more than one element.")
        # pregunta que se le dara al usuario
        self.questions: list[str] = questions
        # respuestas posibles para cada pregunta
        self.answers: list[list[str]] = answers

    def add_question(self, question: str, answer: list[str]) -> None:
        self.questions.append(question)
        self.answers.append(answer)

    def add_answers(self, question: str, answer: str) -> None:
        if question not in self.questions:
            raise ValueError(f'Question "{question}" is not valid.')
        position_question = self.questions.index(question)
        self.answers[position_question].append(answer)

    def send_survey(self, bot, id_to_send, allows_multiple_answers=False):
        if len(self.questions) == 0:
            return
        for question, answers in zip(self.questions, self.answers):
            bot.send_poll(
                chat_id=id_to_send,
                question=question,
                options=answers,
                allows_multiple_answers=allows_multiple_answers,
                is_anonymous=False  # Encuesta no anónima
            )