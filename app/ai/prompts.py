INTENT_CLASSIFICATION_PROMPT = """
You are an AI assistant that classifies incoming emails by intent.

Choose ONE of the following intents:
- product_news
- technical_update
- job_or_career
- marketing_or_spam
- event_or_community

Rules:
- Return ONLY valid JSON
- Do NOT include explanations
- Confidence must be a number between 0 and 1

JSON format:
{{
  "intent": "<one_of_the_intents>",
  "confidence": 0.0
}}


Email content:
----------------
{email_text}
"""

RESPONSE_PROMPTS = {
    "event_or_community": """
You are drafting a polite and professional response to an event or community email.

Write a short acknowledgment showing interest and appreciation.
Do NOT confirm attendance.
Keep it professional and concise.

Email:
{email_text}
""",

    "job_or_career": """
You are drafting a professional response to a job or career-related email.

Politely acknowledge the opportunity.
Do not commit or reject.
Keep it neutral and professional.

Email:
{email_text}
""",

    "product_news": """
Draft a short, neutral acknowledgment response to a product update or newsletter.
Do not ask questions.
Do not sound promotional.

Email:
{email_text}
"""
}
