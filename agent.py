import os
from dotenv import load_dotenv
from typing import List, Tuple

from agno.agent import Agent
from agno.models.groq import Groq
from pydantic import BaseModel, Field

load_dotenv()


class Question(BaseModel):
    question: str = Field(..., description="The question text")
    options: List[str] = Field(
        ..., min_items=4, max_items=4, description="Four answer choices"
    )
    correct_answer: str = Field(
        ..., description="The correct answer (must match one of the options)"
    )


class Quiz(BaseModel):
    title: str = Field(..., description="Title of the quiz")
    questions: List[Question] = Field(
        ..., min_items=10, max_items=10, description="List of 10 quiz questions"
    )


class EvaluationInput(BaseModel):
    """Structured input for evaluating quiz results"""

    questions: List[str] = Field(..., description="List of quiz questions")
    correct_answers: List[str] = Field(
        ..., description="Correct answers for each question"
    )
    user_answers: List[str] = Field(..., description="Answers provided by the student")
    metrics: List[str] = Field(
        ...,
        description="Evaluation metrics like accuracy, weak areas, strengths, suggestions",
    )


class EvaluationReport(BaseModel):
    """Structured output for evaluation results"""

    overview: str = Field(..., description="Overall summary of performance")
    strengths: List[str] = Field(
        ..., description="Areas where the student performed well"
    )
    weak_areas: List[str] = Field(
        ..., description="Topics/questions the student struggled with"
    )
    improvement_suggestions: List[str] = Field(
        ..., description="Actionable tips to improve performance"
    )
    conclusion: str = Field(
        ..., description="Final evaluation and motivational feedback"
    )


# Initialize agent once
agent = Agent(
    model=Groq(api_key=os.getenv("GROQ_API_KEY")),
    output_schema=Quiz,
    description="Generate a 10-question multiple-choice quiz on a given topic or set of topics.",
)

evaluation_agent = Agent(
    model=Groq(api_key=os.getenv("GROQ_API_KEY")),
    output_schema=EvaluationReport,
    description="Evaluate a student's quiz results and provide feedback based on specified metrics.",
)


async def generate_quiz(topic: str) -> Tuple[List[str], List[List[str]], List[str]]:
    """
    Generate a quiz on the given topic and return three lists:
    - questions_list: List of question strings
    - options_list: List of lists (each inner list contains 4 options)
    - answers_list: List of correct answers
    """
    response = await agent.arun(topic)
    quiz: Quiz = response.content  # Cast to Quiz model

    # Separate lists
    questions_list = [q.question for q in quiz.questions]
    options_list = [q.options for q in quiz.questions]
    answers_list = [q.correct_answer for q in quiz.questions]

    return questions_list, options_list, answers_list


async def evaluate_quiz(
    questions: List[str], correct_answers: List[str], user_answers: List[str]
) -> dict:
    """
    Evaluate the quiz results and return a dictionary with evaluation metrics.
    """
    # Compute simple metrics before passing to agent
    total = len(questions)
    correct_count = sum(
        [1 for ca, ua in zip(correct_answers, user_answers) if ca == ua]
    )
    accuracy = (correct_count / total) * 100

    weak_areas = [
        questions[i]
        for i, (ca, ua) in enumerate(zip(correct_answers, user_answers))
        if ca != ua
    ]

    metrics = [
        f"Score: {correct_count}/{total}",
        f"Accuracy: {accuracy:.2f}%",
        f"Weak Areas: {weak_areas if weak_areas else 'None'}",
        "Provide improvement suggestions and highlight strengths.",
    ]

    evaluation_input = EvaluationInput(
        questions=questions,
        correct_answers=correct_answers,
        user_answers=user_answers,
        metrics=metrics,
    )

    eval_response = await evaluation_agent.arun(input=evaluation_input)

    overview = eval_response.content.overview
    strengths = eval_response.content.strengths
    weak_areas = eval_response.content.weak_areas
    improvement_suggestions = eval_response.content.improvement_suggestions
    conclusion = eval_response.content.conclusion

    return {
        "overview": overview,
        "strengths": strengths,
        "weak_areas": weak_areas,
        "improvement_suggestions": improvement_suggestions,
        "conclusion": conclusion,
    }
