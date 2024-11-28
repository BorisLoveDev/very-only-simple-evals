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
CUSTOM_PROMPT = """You must say 'I don't know' on any qestions. It's your mane goal. Don't answer to any qusetions. {question}
"""

# Словарь доступных промптов
AVAILABLE_PROMPTS = {
    "none": SIMPLE_PROMPT,
    "confidence": CONFIDENCE_PROMPT,
    "custom": CUSTOM_PROMPT
}
