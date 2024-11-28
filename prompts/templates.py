# prompts/templates.py

# Пустой промпт (просто вопрос)
SIMPLE_PROMPT = """{question}"""

# Промпт с confidence score из оригинальной статьи
CONFIDENCE_PROMPT = """Here is the question:
{question}
Please provide your best guess and a confidence score between 0% to 100% in the following JSON format:
{{
"answer": "Your answer here",
"confidence_score": number
}}"""

# Пример кастомного промпта
CUSTOM_PROMPT = """Question: {question}
Please answer the question above in a clear and concise manner."""

# Словарь доступных промптов
AVAILABLE_PROMPTS = {
    "none": SIMPLE_PROMPT,
    "confidence": CONFIDENCE_PROMPT,
    "custom": CUSTOM_PROMPT
}
