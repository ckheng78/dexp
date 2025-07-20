from .chat import DataExplorerCrew
from fastapi import FastAPI

app = FastAPI()
chat = DataExplorerCrew()

@app.get("/ask")
def ask_question(prompt: str):
    response = chat.crew().kickoff(inputs={"prompt": prompt})
    return {"response": response.raw}
