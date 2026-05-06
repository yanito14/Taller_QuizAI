import os
import tempfile

from dotenv import load_dotenv
from flask import Flask, redirect, render_template, request, session, url_for

from quiz_generator import generate_questions

load_dotenv()

app = Flask(__name__)
app.secret_key = os.environ.get("FLASK_SECRET_KEY", "clave-secreta-dev")


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/generate", methods=["POST"])
def generate():
    file = request.files.get("pdf")
    n = request.form.get("n", "5")
    difficulty = request.form.get("difficulty", "media")

    if not file or file.filename == "" or not file.filename.lower().endswith(".pdf"):
        return render_template("index.html", error="Por favor sube un archivo PDF válido.")

    try:
        n = int(n)
        if n < 1 or n > 20:
            raise ValueError()
    except ValueError:
        return render_template("index.html", error="El número de preguntas debe ser entre 1 y 20.")

    # Guardar PDF en fichero temporal para procesarlo
    with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp:
        file.save(tmp.name)
        tmp_path = tmp.name

    try:
        questions = generate_questions(tmp_path, n, difficulty)
    except Exception as e:
        return render_template("index.html", error=f"Error al generar preguntas: {e}")
    finally:
        if os.path.exists(tmp_path):
            os.unlink(tmp_path)

    session.clear()
    session["questions"] = questions
    session["current"] = 0
    session["score"] = 0
    session["total"] = len(questions)

    return redirect(url_for("quiz"))


@app.route("/quiz")
def quiz():
    questions = session.get("questions")
    current = session.get("current", 0)
    total = session.get("total", 0)

    if not questions or current >= total:
        return redirect(url_for("results"))

    question = questions[current]
    return render_template("quiz.html", question=question, current=current + 1, total=total)


@app.route("/answer", methods=["POST"])
def answer():
    questions = session.get("questions", [])
    current = session.get("current", 0)

    if current < len(questions):
        correct = questions[current]["Respuesta"]
        user_answer = request.form.get("answer")
        if user_answer == correct:
            session["score"] = session.get("score", 0) + 1
        session["current"] = current + 1

    return redirect(url_for("quiz"))


@app.route("/results")
def results():
    score = session.get("score", 0)
    total = session.get("total", 0)
    return render_template("results.html", score=score, total=total)


@app.route("/restart")
def restart():
    session.clear()
    return redirect(url_for("index"))


if __name__ == "__main__":
    app.run(debug=True)
