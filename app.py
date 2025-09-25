from fastapi import FastAPI
from pydantic import BaseModel
from typing import List, Dict, Any
from fastapi.middleware.cors import CORSMiddleware  # Add this import

from agent import generate_quiz, evaluate_quiz

app = FastAPI()

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)


# --- Request/Response Schemas ---
class QuizRequest(BaseModel):
    topic: str


class QuizResponse(BaseModel):
    questions: List[str]
    options: List[List[str]]
    answers: List[str]


class EvaluateRequest(BaseModel):
    questions: List[str]
    correct_answers: List[str]
    user_answers: List[str]
    metrics: List[str]


class EvaluateResponse(BaseModel):
    overview: str
    strengths: List[str]
    weak_areas: List[str]
    improvement_suggestions: List[str]
    conclusion: str


# --- Endpoints ---
@app.get("/", response_model=Dict[str, str])
def read_root():
    """
    Root endpoint for the Codify AI server.
    """
    return {"message": "Welcome to the Codify AI server!"}


@app.post("/quiz", response_model=QuizResponse)
async def create_quiz(request: QuizRequest):
    """
    Generate a quiz on a given topic.
    """
    questions, options, answers = await generate_quiz(request.topic)
    return QuizResponse(questions=questions, options=options, answers=answers)


@app.post("/evaluate", response_model=EvaluateResponse)
async def evaluate(request: EvaluateRequest):
    """
    Evaluate quiz results.
    """
    evaluation_results = await evaluate_quiz(
        request.questions,
        request.correct_answers,
        request.user_answers,
        request.metrics,
    )
    return evaluation_results
