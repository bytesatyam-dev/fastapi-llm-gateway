FastAPI LLM Gateway
A production-style API gateway for interacting with large language models, built with FastAPI and Groq. Goes beyond a simple Q&A wrapper — supports multi-turn conversations, configurable system prompts, and runtime model selection.
Why This Exists
Most LLM integrations are tightly coupled to a single provider and a single use case. This project demonstrates how to build a clean, extensible gateway layer that separates transport concerns from AI provider logic — making it easy to swap models or providers without touching business logic.
Features

Multi-turn conversation support via message history
Configurable system prompts per request
Runtime model selection from supported Groq models
Input validation with Pydantic — only valid roles accepted
Structured error handling with meaningful HTTP responses
Request logging for observability
Environment-based config — no hardcoded secrets

Tech Stack

Framework: FastAPI
LLM Provider: Groq (LLaMA 3.3 70B, LLaMA 3.1 8B, Gemma2 9B)
Validation: Pydantic
Config: python-dotenv

Getting Started
bashgit clone https://github.com/bytesatyam-dev/fastapi-llm-gateway.git
cd fastapi-llm-gateway
pip install -r requirements.txt
cp .env.sample .env
# Add your GROQ_API_KEY to .env
uvicorn main:app --reload
API docs at http://localhost:8000/docs
API
MethodEndpointDescriptionPOST/chatMulti-turn chat with model and system prompt selectionGET/modelsList available modelsGET/healthService health check
Design Decisions

Message role validation — enforces user/assistant only, catches bad requests early
503 on provider failure — treats Groq as external dependency, not core infrastructure
System prompt per request — allows different AI personas without separate deployments
