class Question:

    keywords = None
    question = None
    answer = None

    def __init__(self, question, answer):
        self.question = question
        self.answer = [answer]

    def set_keywords(self, keywords):
        self.keywords = keywords

    def add_answer(self, answer):
        self.answer.append(answer)