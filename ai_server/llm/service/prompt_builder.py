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

    def build_prompt(self, query: str) -> str:
        prefer_info = ""
        for i in range(1, 20):
            key = f"Q_{i}"
            value = self.prefer.get(key)
            if value:
                prefer_info += f"- Q{i}: {value}\n"

        weather_info = self.build_weather_context()

        return f"""
    📋 [사용자 선호 정보]
    {prefer_info if prefer_info else '정보 없음'}

    🌦️ [현재 날씨 정보]
    {weather_info}

    🗣 [질문]
    {query}

    위 정보를 바탕으로 적절한 메뉴와 식당을 추천해주세요.
    """
