from fastapi import FastAPI
from dotenv import load_dotenv
import uvicorn
import os

from config.cors_config import CorsConfig
from weather.controller.weather_controller import weatherRouter
from chat_history.controller.chat_history_controller import chatHistoryRouter
from llm.controller.llm_controller import llmRouter

load_dotenv()

app = FastAPI()

CorsConfig.middlewareConfig(app)

app.include_router(weatherRouter)
app.include_router(chatHistoryRouter)
app.include_router(llmRouter)


if __name__ == "__main__":
    uvicorn.run(app, host=os.getenv('HOST'), port=int(os.getenv('FASTAPI_PORT')))