import os
import json
import logging
import webbrowser
import threading
from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
from groq import Groq
from dotenv import load_dotenv

load_dotenv()

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
logger = logging.getLogger(__name__)

app = Flask(__name__, static_folder='static', template_folder='templates')
CORS(app)

GROQ_API_KEY = os.environ.get("GROQ_API_KEY")
if not GROQ_API_KEY:
    raise EnvironmentError("GROQ_API_KEY not found. Add it to your .env file.")

client = Groq(api_key=GROQ_API_KEY)


def ask_ai(prompt: str, max_tokens: int = 1024) -> str:
    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[{"role": "user", "content": prompt}],
        max_tokens=max_tokens,
        temperature=0.7
    )
    return response.choices[0].message.content.strip()


def extract_json(raw: str):
    raw = raw.strip()
    if raw.startswith("```"):
        parts = raw.split("```")
        raw = parts[1] if len(parts) > 1 else raw
        if raw.startswith("json"):
            raw = raw[4:]
    return json.loads(raw.strip())


# ── Page Routes ──
@app.route("/")
def index():
    return render_template("index.html")

@app.route("/ask")
def ask_page():
    return render_template("ask.html")

@app.route("/explain")
def explain_page():
    return render_template("explain.html")

@app.route("/quiz")
def quiz_page():
    return render_template("quiz.html")

@app.route("/summary")
def summary_page():
    return render_template("summary.html")

@app.route("/test")
def test_page():
    return render_template("test.html")

@app.route("/flashcards")
def flashcards_page():
    return render_template("flashcards.html")

@app.route("/translate")
def translate_page():
    return render_template("translate.html")


# ── Feature 1: Smart Q&A ──
@app.route("/ask", methods=["POST"])
def ask_question():
    data = request.get_json(silent=True)
    if not data or not data.get("question", "").strip():
        return jsonify({"error": "Field 'question' is required."}), 400
    question = data["question"].strip()
    subject  = data.get("subject", "general knowledge").strip() or "general knowledge"
    prompt = f"""You are EduGenie, a knowledgeable and friendly academic assistant.
A student is asking a {subject} question. Provide a clear, accurate, and structured answer.
Use bullet points or numbered steps where helpful. Keep language simple and student-friendly.
Question: {question}
Answer:"""
    try:
        answer = ask_ai(prompt)
        return jsonify({"question": question, "subject": subject, "answer": answer})
    except Exception as e:
        logger.error(e)
        return jsonify({"error": "AI failed to generate an answer. Try again."}), 500


# ── Feature 2: Concept Explanation ──
@app.route("/explain", methods=["POST"])
def explain_concept():
    data = request.get_json(silent=True)
    if not data or not data.get("concept", "").strip():
        return jsonify({"error": "Field 'concept' is required."}), 400
    concept = data["concept"].strip()
    level   = data.get("level", "beginner").strip().lower()
    if level not in ("beginner", "intermediate", "advanced"):
        level = "beginner"
    prompt = f"""You are EduGenie. Explain "{concept}" to a {level}-level student.
📌 Definition: (one clear sentence)
🔍 Analogy: (relatable real-world comparison)
✅ Key Points: (3-5 bullet points)
💡 Fun Fact: (one interesting insight)"""
    try:
        explanation = ask_ai(prompt)
        return jsonify({"concept": concept, "level": level, "explanation": explanation})
    except Exception as e:
        logger.error(e)
        return jsonify({"error": "AI failed to generate an explanation. Try again."}), 500


# ── Feature 3: Quiz Generation ──
@app.route("/quiz", methods=["POST"])
def generate_quiz():
    data = request.get_json(silent=True)
    if not data or not data.get("topic", "").strip():
        return jsonify({"error": "Field 'topic' is required."}), 400
    topic         = data["topic"].strip()
    num_questions = min(int(data.get("num_questions", 5)), 10)
    difficulty    = data.get("difficulty", "medium").strip().lower()
    prompt = f"""Generate exactly {num_questions} MCQs on "{topic}". Difficulty: {difficulty}.
Return ONLY a JSON array. Each item:
{{"question_number":1,"question":"?","options":{{"A":"","B":"","C":"","D":""}},"correct_answer":"A","explanation":""}}
Only the JSON array."""
    try:
        raw       = ask_ai(prompt)
        questions = extract_json(raw)
        return jsonify({"topic": topic, "difficulty": difficulty, "num_questions": len(questions), "quiz": questions})
    except Exception as e:
        logger.error(e)
        return jsonify({"error": "AI failed to generate quiz. Try again."}), 500


# ── Feature 4: Content Summarizer ──
@app.route("/summary", methods=["POST"])
def summarize_content():
    data = request.get_json(silent=True)
    if not data or not data.get("content", "").strip():
        return jsonify({"error": "Field 'content' is required."}), 400
    content = data["content"].strip()
    if len(content) < 50:
        return jsonify({"error": "Please provide at least 50 characters."}), 400
    prompt = f"""Summarize this study material clearly:
📝 Overview: (2-3 sentences)
🔑 Key Points: (bullet points)
📚 Important Terms: (with definitions)
🎯 Takeaway: (one sentence)
Material: {content}"""
    try:
        summary = ask_ai(prompt)
        return jsonify({"summary": summary, "char_count": len(content)})
    except Exception as e:
        logger.error(e)
        return jsonify({"error": "AI failed to summarize. Try again."}), 500


# ── Feature 5: Test Mode - Generate ──
@app.route("/test/generate", methods=["POST"])
def generate_test():
    data = request.get_json(silent=True)
    if not data or not data.get("topic", "").strip():
        return jsonify({"error": "Field 'topic' is required."}), 400
    topic         = data["topic"].strip()
    num_questions = min(int(data.get("num_questions", 5)), 10)
    difficulty    = data.get("difficulty", "medium").strip().lower()
    prompt = f"""Generate exactly {num_questions} short-answer test questions on "{topic}". Difficulty: {difficulty}.
Return ONLY a JSON array. Each item:
{{"question_number":1,"question":"?","correct_answer":"1-3 sentence answer","keywords":["key1","key2","key3"]}}
Only the JSON array."""
    try:
        raw       = ask_ai(prompt)
        questions = extract_json(raw)
        return jsonify({"topic": topic, "difficulty": difficulty, "questions": questions})
    except Exception as e:
        logger.error(e)
        return jsonify({"error": "AI failed to generate test. Try again."}), 500


# ── Feature 5: Test Mode - Validate ──
@app.route("/test/validate", methods=["POST"])
def validate_answer():
    data = request.get_json(silent=True)
    if not data:
        return jsonify({"error": "Invalid request."}), 400
    question       = data.get("question", "")
    student_answer = data.get("student_answer", "").strip()
    correct_answer = data.get("correct_answer", "")
    keywords       = data.get("keywords", [])
    if not student_answer:
        return jsonify({"error": "Please write an answer before submitting."}), 400
    prompt = f"""You are an expert teacher grading a student's answer.
Question: {question}
Correct Answer: {correct_answer}
Key Concepts: {', '.join(keywords)}
Student Answer: {student_answer}

Respond ONLY with this JSON:
{{"score":85,"grade":"B","is_correct":true,"feedback":"Your feedback here","correct_answer":"Full correct answer","tips":"Study tip here"}}
Score 0-100. Grade A(90-100) B(75-89) C(60-74) D(40-59) F(0-39). is_correct true if score>=60."""
    try:
        raw    = ask_ai(prompt)
        result = extract_json(raw)
        return jsonify(result)
    except Exception as e:
        logger.error(e)
        return jsonify({"error": "Failed to validate answer. Try again."}), 500


# ── Feature 6: Flashcards ──
@app.route("/flashcards/generate", methods=["POST"])
def generate_flashcards():
    data = request.get_json(silent=True)
    if not data or not data.get("topic", "").strip():
        return jsonify({"error": "Field 'topic' is required."}), 400
    topic = data["topic"].strip()
    count = min(int(data.get("count", 10)), 20)
    prompt = f"""Generate exactly {count} flashcards for studying "{topic}".
Return ONLY a JSON array. Each item:
{{"id":1,"front":"Term or question","back":"Definition or answer"}}
Only the JSON array."""
    try:
        raw   = ask_ai(prompt)
        cards = extract_json(raw)
        return jsonify({"topic": topic, "count": len(cards), "flashcards": cards})
    except Exception as e:
        logger.error(e)
        return jsonify({"error": "Failed to generate flashcards. Try again."}), 500


# ── Feature 7: Translate & Simplify ──
@app.route("/translate", methods=["POST"])
def translate_content():
    data = request.get_json(silent=True)
    if not data or not data.get("content", "").strip():
        return jsonify({"error": "Field 'content' is required."}), 400
    content  = data["content"].strip()
    language = data.get("language", "Simple English").strip()
    prompt = f"""Rewrite or translate the following study content into {language}.
Make it easy to understand, clear, and student-friendly.
Content: {content}
Rewritten in {language}:"""
    try:
        result = ask_ai(prompt)
        return jsonify({"result": result, "language": language})
    except Exception as e:
        logger.error(e)
        return jsonify({"error": "Failed to translate. Try again."}), 500


# ── Error Handlers ──
@app.errorhandler(404)
def not_found(e):
    return jsonify({"error": "Route not found."}), 404

@app.errorhandler(500)
def server_error(e):
    return jsonify({"error": "Internal server error."}), 500


if __name__ == "__main__":
    port  = int(os.environ.get("PORT", 8080))
    debug = os.environ.get("FLASK_DEBUG", "false").lower() == "true"
    url   = f"http://localhost:{port}"

    def open_browser():
        webbrowser.open(url)

    threading.Timer(1.0, open_browser).start()
    logger.info(f"🚀 EduGenie running on {url}")
    app.run(host="0.0.0.0", port=port, debug=debug, use_reloader=False)