from fastapi import FastAPI , Depends , HTTPException , Query
from sqlalchemy.orm import Session
from app.db.sessions import SessionLocal
from app.db.models import Email

app = FastAPI(title="AI Email Agent")

def get_db():
    db = SessionLocal()
    try : 
        yield db
    finally:
        db.close()


@app.get('/email')
def get_all_emails(db: Session= Depends(get_db)):
    return db.query(Email).all()

@app.get("/email/{email_id}")
async def get_email_by_id(email_id : int , db: Session=Depends(get_db)):
    emails = db.query(Email).filter(Email.id == email_id).first()

    if not emails:
        raise HTTPException(status_code=404 , detail="Email not found")
    
    return emails

@app.get("/emails/status")
async def get_emails_by_status(status:str = Query(... , description="Email status to filter by"),
                               db : Session=Depends(get_db) ):
    emails = db.query(Email).filter(Email.status == status).all()
    if not emails : 
        raise HTTPException(status_code=404 , detail = "Status not found")
    
    return emails 