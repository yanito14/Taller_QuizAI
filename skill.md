<Skill_1>
<Fomarto_Salida>
[
  {
    "Pregunta": "¿Cuál es la capital de Francia?",
    "Opciones": [["a", "París"], ["b", "Londres"], ["c", "Roma"], ["d", "Berlín"]],
    "Respuesta": "a"
  }
]
</Fomarto_Salida>
</Skill_1>

===================== DOS FORMATOS DE DE SKILL =====================

# Skill_1 Generador de preguntas

## Descripción
.......

## Rol
Actua como un profesor .....

## Instrucciones
1. Genera preguntas {numero_preguntas} de la dificultad {dificultad} sobre el {texto}.
2. Cada pregunta debe tener 4 opciones de respuesta, etiquetadas como a, b, c y d.
3. Cada pregunta solo tiene una respuesta valida.
4. No quiero que las preguntas sean obvia 

## Entrada
{texto}

## Salida
Una lista de preguntas en formato json, siguiendo siempre este formato:
[
  {
    "Pregunta": "¿Cuál es la capital de Francia?",
    "Opciones": [["a", "París"], ["b", "Londres"], ["c", "Roma"], ["d", "Berlín"]],
    "Respuesta": "a"
  },
  ...
]