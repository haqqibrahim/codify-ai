# Codify AI Server

A FastAPI-based quiz generator and evaluator powered by AI agents.

---

## 🚀 Setup & Installation

1. **Clone the repository**
    ```bash
    git clone https://github.com/your-username/codify-ai.git
    cd codify-ai
    ```

2. **Create a virtual environment**
    ```bash
    # For Linux/Mac
    python3 -m venv venv
    source venv/bin/activate

    # For Windows (PowerShell)
    python -m venv venv
    .\venv\Scripts\activate
    ```

3. **Install dependencies**
    ```bash
    pip install -r requirements.txt
    ```

4. **Run the app**
    ```bash
    uvicorn main:app --reload
    ```
    The server will start at:  
    👉 [http://127.0.0.1:8000](http://127.0.0.1:8000)

---

## 📘 API Documentation

FastAPI auto-generates Swagger UI and ReDoc documentation:

- Swagger UI → [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)
- ReDoc → [http://127.0.0.1:8000/redoc](http://127.0.0.1:8000/redoc)

---

## ⚡ Endpoints

### 1. Root

**`GET /`**  
Returns a welcome message.

**Response**:
```json
{
  "message": "Welcome to the Codify AI server!"
}
```

---

### 2. Generate Quiz

**`POST /quiz`**  
Generates a quiz on a given topic.

**Request Body**:
```json
{
  "topic": "Python programming"
}
```

**Response**:
```json
{
  "questions": [
     "What is a Python list?",
     "Which keyword defines a function in Python?"
  ],
  "options": [
     ["A mutable sequence", "An immutable sequence", "A number", "A string"],
     ["def", "func", "function", "lambda"]
  ],
  "answers": [
     "A mutable sequence",
     "def"
  ]
}
```

---

### 3. Evaluate Quiz

**`POST /evaluate`**  
Evaluates user answers and provides structured feedback.

**Request Body**:
```json
{
  "questions": [
     "What is a Python list?",
     "Which keyword defines a function in Python?"
  ],
  "correct_answers": [
     "A mutable sequence",
     "def"
  ],
  "user_answers": [
     "A string",
     "def"
  ],
  "metrics":[
    "response time per question: 20 secs",
    "memory retention: 45%"
  ]
}
```

**Response**:
```json
{
  "overview": "You answered 1/2 questions correctly. Accuracy: 50%.",
  "strengths": ["You understood how to define functions using 'def'."],
  "weak_areas": ["Confusion about Python list mutability."],
  "improvement_suggestions": ["Review Python's built-in data structures."],
  "conclusion": "Good start! Strengthen your understanding of collections."
}
```

---

✅ That way, anyone can just follow the steps, run the server, and play with the endpoints on Swagger UI.

---

Do you want me to also **generate a sample `requirements.txt`** for you (with FastAPI, Uvicorn, Pydantic, etc.), or do you already have one?