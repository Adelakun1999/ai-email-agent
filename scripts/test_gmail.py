from app.email.gmail_client import (
    fetch_unread_emails,
    get_message,
    parse_email,
    get_gmail_services
)
from app.workflows.email_pipeline import store_email


service = get_gmail_services()
messages = fetch_unread_emails()

for msg in messages:
    full_msg = get_message(service, msg["id"])
    parsed = parse_email(full_msg)

    stored = store_email(parsed)

    if stored:
        print("Stored:", parsed["subject"])
    else:
        print("Skipped duplicate:", parsed["subject"])