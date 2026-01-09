from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build 
from google.auth.transport.requests import Request
import pickle
import os 
import base64
from email.utils import parseaddr

from bs4 import BeautifulSoup
import re 


SCOPES = ["https://www.googleapis.com/auth/gmail.readonly"]

def get_gmail_services():
    creds = None 

    if os.path.exists("token.pickle"):
        with open("token.pickle" ,"rb") as token :
            creds = pickle.load(token)

    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else : 
            flow = InstalledAppFlow.from_client_secrets_file(
                "credentials.json" , SCOPES
            )
            creds = flow.run_local_server(port=0)

        with open("token.pickle" , "wb") as token:
            pickle.dump(creds, token)

    service = build("gmail", "v1", credentials=creds)
    return service


def fetch_unread_emails(max_results = 5):
    service = get_gmail_services()

    results = service.users().messages().list(
        userId = "me",
        labelIds = ["INBOX", 'UNREAD'],
        maxResults = max_results
    ).execute()

    messages = results.get("messages" , [])
    return messages


def get_message(service, message_id):
    return service.users().messages().get(
        userId = "me",
        id = message_id,
        format = "full"
    ).execute()


def extract_headers(payload):
    headers = payload.get("headers" , [])
    data = {}

    for header in headers:
        name = header["name"].lower()
        if name == "from":
            data['from'] = parseaddr(header['value'])[1]
        elif name == "subject":
            data['subject'] = header['value']

    return data

from bs4 import BeautifulSoup

def html_to_text(html):
    soup = BeautifulSoup(html, "html.parser")

    # Remove everything that is not visible text
    for tag in soup(["style", "script", "head", "meta", "title", "link"]):
        tag.decompose()

    # Remove extra whitespace
    text = soup.get_text(separator=" ", strip=True)

    # Optional: collapse multiple spaces/newlines
    text = re.sub(r'\s+', ' ', text)

    return text


def extract_body(payload):
    if "parts" in payload:
        for part in payload["parts"]:
            mime_type = part.get("mimeType", "")

            if mime_type == "text/plain":
                return decode_body(part["body"])

            if mime_type == "text/html":
                html = decode_body(part["body"])
                return html_to_text(html)

            if mime_type.startswith("multipart"):
                text = extract_body(part)
                if text:
                    return text
    else:
        return decode_body(payload.get("body", {}))

    return ""


def decode_body(body):
    data = body.get("data")
    if not data:
        return ""

    decoded_bytes = base64.urlsafe_b64decode(data)
    return decoded_bytes.decode("utf-8", errors="ignore")


def parse_email(message):
    payload = message["payload"]

    headers = extract_headers(payload)
    body = extract_body(payload)

    return {
        "message_id": message["id"],
        "from": headers.get("from", ""),
        "subject": headers.get("subject", ""),
        "body": body.strip()
    }
