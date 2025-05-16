import os
from dotenv import load_dotenv
from langsmith import Client
import matplotlib.pyplot as plt

load_dotenv()
client = Client(api_key=os.getenv("LANGCHAIN_API_KEY"))

runs = client.list_runs(project_name="hungll", run_type="llm")

latencies = []
tokens = []
timestamps = []

for run in runs:
    # ✅ latency 직접 계산
    if run.start_time and run.end_time:
        latency = (run.end_time - run.start_time).total_seconds()
    else:
        latency = 0
    latencies.append(latency)

    # ✅ 토큰 정보가 없을 경우 0 처리
    tokens.append(run.total_tokens or 0)
    timestamps.append(run.start_time.strftime("%Y-%m-%d %H:%M") if run.start_time else "unknown")

# 📊 시각화
plt.figure(figsize=(12, 6))
plt.plot(timestamps, latencies, label="Latency (s)", marker='o')
plt.plot(timestamps, tokens, label="Total Tokens", marker='x')
plt.xlabel("Timestamp")
plt.ylabel("Value")
plt.title("LangSmith 실험 로그 요약")
plt.legend()
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()
