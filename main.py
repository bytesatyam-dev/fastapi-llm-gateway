from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from groq import Groq
from dotenv import load_dotenv
import os
import logging

load_dotenv()

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI()
client = Groq(api_key=os.getenv("GROQ_API_KEY"))

class QuestionRequest(BaseModel):
    question: str

class AnswerResponse(BaseModel):
    answer: str

@app.post("/ask", response_model=AnswerResponse)
async def ask_question(request: QuestionRequest):
    try:
        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {"role": "user", "content": request.question}
            ]
        )
        return AnswerResponse(answer=response.choices[0].message.content)
    except Exception as e:
        logger.error(f"LLM call failed: {str(e)}")
        raise HTTPException(
            status_code=503,
            detail="AI service unavailable. Please try again later."
        )

@app.get("/health")
async def health():
    return {"status": "ok"}