from app.db.sessions import SessionLocal
from app.db.models import Email

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