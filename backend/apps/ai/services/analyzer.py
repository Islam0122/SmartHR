from ..clients.gigachat import GigaChatClient


class VacancyAIAnalyzer:

    def __init__(self):
        self.client = GigaChatClient()

    def analyze_candidate(self, vacancy, candidate_answers: dict) -> dict:
        prompt = f"""
Ты HR AI ассистент.

Вакансия:
Название: {vacancy.title}
Требования: {vacancy.requirements}
Навыки: {vacancy.skills}

Ответы кандидата:
{candidate_answers}

Верни JSON:
score (0-100)
strengths
weaknesses
summary
"""

        response = self.client.ask(prompt)
        return response
