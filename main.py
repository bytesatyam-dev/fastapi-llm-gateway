from typing import Literal
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from groq import Groq
from dotenv import load_dotenv
import os
import logging

load_dotenv()

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(title="FastAPI LLM Gateway")
client = Groq(api_key=os.getenv("GROQ_API_KEY"))

AVAILABLE_MODELS = [
    "llama-3.3-70b-versatile",
    "llama-3.1-8b-instant",
    "gemma2-9b-it"
]

class Message(BaseModel):
    role: Literal["user", "assistant"]
    content: str

class ChatRequest(BaseModel):
    messages: list[Message]
    system_prompt: str = "You are a helpful assistant."
    model: str = "llama-3.3-70b-versatile"

class ChatResponse(BaseModel):
    reply: str
    model_used: str

@app.post("/chat", response_model=ChatResponse)
async def chat(request: ChatRequest):
    if request.model not in AVAILABLE_MODELS:
        raise HTTPException(
            status_code=400,
            detail=f"Invalid model. Choose from: {AVAILABLE_MODELS}"
        )
    try:
        messages = [{"role": "system", "content": request.system_prompt}]
        messages += [{"role": m.role, "content": m.content} for m in request.messages]

        response = client.chat.completions.create(
            model=request.model,
            messages=messages
        )
        return ChatResponse(
            reply=response.choices[0].message.content,
            model_used=request.model
        )
    except Exception as e:
        logger.error(f"LLM call failed: {str(e)}")
        raise HTTPException(
            status_code=503,
            detail="AI service unavailable. Please try again later."
        )

@app.get("/models")
async def list_models():
    return {"available_models": AVAILABLE_MODELS}

@app.get("/health")
async def health():
    return {"status": "ok"}