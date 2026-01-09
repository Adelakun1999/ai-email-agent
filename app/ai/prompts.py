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