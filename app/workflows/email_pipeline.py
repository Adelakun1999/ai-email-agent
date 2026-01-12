from app.db.sessions import SessionLocal
from app.db.models import Email
from app.ai.classifier import classify_email_intent
from app.ai.responder import generate_draft_response
import logging  


CONFIDENCE_THRESHOLD = 0.6 

logging.basicConfig(
    level= logging.INFO,
     format="%(asctime)s [%(levelname)s] %(message)s"
)

logger = logging.getLogger(__name__)




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
    logger.info(f"Found {len(emails)} unclassified emails")

    for email in emails:
        email_text = f"""
        FROM : {email.sender}

        Subject : {email.subject}

         {email.body}
         
        """

        result = classify_email_intent(email_text)
        email.intent = result['intent']
        email.confidence = result['confidence']
        email.status = 'classified'

        logger.info(
            f"Email ID {email.id} classified as '{email.intent}' with confidence {email.confidence}"
        )


        print(f"Updated {email.id}: {email.intent} ({email.confidence})")

    db.commit()
    db.close()

def apply_decision_logic():
    """
    Applies rules to all classified emails:
      - skip spam 
      - Mark low-confidence emails for review 
      - Generate draft for high-confidence relevant emails
    Updates draft_response and status
    """

    db = SessionLocal()
    emails = db.query(Email).filter(Email.status == "classified").all()
    logger.info(f"Applying decision logic to {len(emails)} classified emails.")
    for email in emails:
        # skip marketing/spam emails
        if email.intent == "marketing_or_spam":
            email.status = "skipped"
            logger.info(f"Email ID {email.id} skipped (spam)")
            continue

        if email.confidence is not None and email.confidence < CONFIDENCE_THRESHOLD:
            email.status = "review"
            logger.info(
                f"Email ID {email.id} marked for review (low confidence: {email.confidence})."
            )

            continue


        # Generate draft for valid high confidence email
        email_text = f"""
From: {email.sender}
Subject: {email.subject}

{email.body}
"""
        draft = generate_draft_response(
            intent=email.intent,
            email_text=email_text
        )

        if draft:
            email.draft_response = draft
            email.status = "drafted"
            logger.info(f"Email ID {email.id} drafted (intent: {email.intent}).")

    db.commit()
    db.close()
    logger.info("Decision logic complete.")




if __name__ == "__main__":
    logger.info("Starting email pipeline")
    #classify_parsed_email()
    apply_decision_logic()
    logger.info("Email pipeline finished")
        


