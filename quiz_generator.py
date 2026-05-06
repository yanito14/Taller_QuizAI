import os
import json
from pathlib import Path

import pypdf
from openai import OpenAI
#   import ollama


def extract_text_from_pdf(pdf_path):
    text = ""
    with open(pdf_path, "rb") as f:
        reader = pypdf.PdfReader(f)
        for page in reader.pages:
            text += page.extract_text() or ""
    return text.strip()


def load_skill():
    skill_path = Path(__file__).parent / "skill.md"
    return skill_path.read_text(encoding="utf-8")


def generate_questions(pdf_path, n, difficulty):
    client = OpenAI(api_key=os.environ["OPENAI_API_KEY"])

    text = extract_text_from_pdf(pdf_path)
    if not text:
        raise ValueError("No se pudo extraer texto del PDF.")

    skill = load_skill()
    user_prompt = (
        f"Genera {n} preguntas de dificultad '{difficulty}' "
        f"basadas en el siguiente texto:\n\n{text}"
    )

# ESTA PARTE ES LA QUE TENEIS QUE RELLENAR VOSOTROS
    response = client.chat.completions.create(
        model="gpt-5.4o-mini",
        messages=[
            {"role": "system", "content": skill},
            {"role": "user", "content": user_prompt},
        ],
        response_format={"type": "json_object"},
        temperature=0.7,
    )
###

    data = json.loads(response.choices[0].message.content)

    # Extraer la lista de preguntas sea cual sea la clave del objeto
    if isinstance(data, list):
        return data
    for value in data.values():
        if isinstance(value, list):
            return value

    raise ValueError("La API no devolvió el formato JSON esperado.")


# ESTA TAMBIEN LA TENÉIS QUE RELLENAR VOSOTROS
def generate_questions_with_ollama(pdf_path, n, difficulty):
    raise NotImplementedError("La función generate_questions_with_ollama no está implementada.")