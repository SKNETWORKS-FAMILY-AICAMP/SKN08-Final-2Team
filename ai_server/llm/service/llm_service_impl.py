import os
from rag.embedder import get_embedding
from rag.faiss_index import search as faiss_search
from langchain_core.tracers import LangChainTracer
from langchain_openai import ChatOpenAI


class LLMServiceImpl:
    def __init__(self):
        self.tracer = LangChainTracer(project_name=os.getenv("LANGCHAIN_PROJECT"))
        self.llm = ChatOpenAI(
            api_key=os.getenv("OPENAI_API_KEY"),
            streaming=True,
            temperature=0.7,
            callbacks=[self.tracer],
            model="gpt-3.5-turbo"
        )

    def get_streaming_openai_response(self, prompt: str):
        print(f"🔍 프롬프트:\n{prompt}")

        try:
            # RAG 적용
            embedding = get_embedding(prompt)
            related_restaurants = faiss_search(embedding, top_k=3)

            restaurant_info = "\n".join([
                f"- {r['name']} ({r['address']})" for r in related_restaurants
            ])
            prompt += f"\n\n📌 [참고 가능한 식당 정보]\n{restaurant_info}"

            # Streaming 응답 generator 반환
            return self.llm.stream(prompt)

        except Exception as e:
            print(f"❌ OpenAI 스트리밍 실패: {e}")
            return iter([])  # 빈 generator 반환
