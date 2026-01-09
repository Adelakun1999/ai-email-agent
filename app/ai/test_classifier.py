from app.ai.classifier import classify_email_intent

sample_email = """
Subject: NVIDIA at CES 2026 recap

We announced Rubin, Alpamayo, and several new GPUs for developers
"""

result = classify_email_intent(sample_email)
print(result)
