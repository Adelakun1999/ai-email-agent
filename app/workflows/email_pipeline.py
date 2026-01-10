from app.db.sessions import SessionLocal
from app.db.models import Email
from app.ai.classifier import classify_email_intent

def store_email(email_data):
    db = SessionLocal()

    exists = db.query(Email).filter(
        Email.message_id == email_data["message_id"]
    ).first()

    if exists:
        db.close()
        return False
    
    
    email = Email(
        message_id=email_data["message_id"],
        sender=email_data["from"],
        subject=email_data["subject"],
        body=email_data["body"],
    )

    db.add(email)
    db.commit()
    db.close()

    return True

def classify_parsed_email():
    db = SessionLocal()

    emails = db.query(Email).filter(Email.intent==None).all()

    for email in emails:
        email_text = f"""
        FROM : {email.sender}

        Subject : {email.subject}

         {email.body}
         
        """

        result = classify_email_intent(email_text)
        email.intent = result['intent']
        email.confidence = result['confidence']

        print(f"Updated {email.id}: {email.intent} ({email.confidence})")

    db.commit()
    db.close()