from llm.service.prefer_question_map import PREFERENCE_QUESTIONS

class PromptBuilder:
    def __init__(self, prefer_model, weather: dict = None):
        self.prefer = prefer_model
        self.weather = weather or {}

    def build_preference_context(self) -> str:
        lines = []
        for q_key, question in PREFERENCE_QUESTIONS.items():
            answer = getattr(self.prefer, q_key, None)
            if answer:
                lines.append(f"- {question}: {answer}")
        return "\n".join(lines)

    def build_weather_context(self) -> str:
        return "\n".join([f"- {k}: {v}" for k, v in self.weather.items()])

    def build_prompt(self, user_question: str) -> str:
        return f"""
        📋 [사용자 선호 정보]
        {self.build_preference_context()}

        🌦️ [현재 날씨 정보]
        {self.build_weather_context()}

        🗣 [질문]
        {user_question}

        위 정보를 바탕으로 적절한 메뉴와 식당을 추천해주세요.
        """
