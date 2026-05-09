import os
import base64
import time
import re

from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email import encoders

from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from google.oauth2.credentials import Credentials

from dotenv import load_dotenv
from app.memory.store import get_conversation
from app.reply.chat import process_message

load_dotenv()

SCOPES = ["https://www.googleapis.com/auth/gmail.modify"]
EMAIL = os.getenv("EMAIL")


def generate_gmail_token():
    flow = InstalledAppFlow.from_client_secrets_file(
        os.getenv("OAUTH_CREDENTIALS_FILE"),
        SCOPES,
    )

    creds = flow.run_local_server(port=0)

    with open(os.getenv("TOKEN_FILE"), "w") as token:
        token.write(creds.to_json())

    print("Token generated and saved")


def get_gmail_service():
    creds = Credentials.from_authorized_user_file(os.getenv("TOKEN_FILE"), SCOPES)
    return build("gmail", "v1", credentials=creds)


def get_unread_messages(service):
    results = (
        service.users()
        .messages()
        .list(userId="me", labelIds=["UNREAD"], maxResults=5)
        .execute()
    )
    return results.get("messages", [])


def get_email_details(service, msg_id):
    message = service.users().messages().get(userId="me", id=msg_id).execute()
    headers = message["payload"]["headers"]

    subject = next((h["value"] for h in headers if h["name"] == "Subject"), "")
    sender = next((h["value"] for h in headers if h["name"] == "From"), "")

    body = ""

    try:
        if "parts" in message["payload"]:
            for part in message["payload"]["parts"]:
                if part["mimeType"] == "text/plain":
                    data = part["body"]["data"]
                    body = base64.urlsafe_b64decode(data).decode()
                    break
        else:
            data = message["payload"]["body"]["data"]
            body = base64.urlsafe_b64decode(data).decode()
    except Exception as e:
        print("Error decoding email:", e)

    return sender, subject, body


def clean_email(text):

    lines = text.splitlines()

    cleaned_lines = []

    STOP_PREFIXES = (
        "on ",
        "from:",
        "sent:",
        "subject:",
        ">",
    )

    for line in lines:

        stripped = line.strip()

        if not stripped:
            continue
        if stripped.lower().startswith(STOP_PREFIXES):
            break

        if stripped.startswith("___"):
            continue

        cleaned_lines.append(stripped)

    cleaned = " ".join(cleaned_lines)

    return cleaned[:300]


def send_reply(service, to, subject, body):
    message = MIMEText(body)
    message["to"] = to
    message["subject"] = "Re: " + subject

    raw = base64.urlsafe_b64encode(message.as_bytes()).decode()

    service.users().messages().send(userId="me", body={"raw": raw}).execute()
    print("Reply sent via email")


def send_file_email(service, to, subject, file_path):
    message = MIMEMultipart()
    message["to"] = to
    message["subject"] = "Requested File"

    with open(file_path, "rb") as f:
        part = MIMEBase("application", "octet-stream")
        part.set_payload(f.read())

    encoders.encode_base64(part)

    part.add_header(
        "Content-Disposition",
        f'attachment; filename="{os.path.basename(file_path)}"',
    )

    message.attach(part)

    raw = base64.urlsafe_b64encode(message.as_bytes()).decode()

    service.users().messages().send(userId="me", body={"raw": raw}).execute()

    print("File sent via email")


def auto_reply():
    service = get_gmail_service()
    messages = get_unread_messages(service)

    if not messages:
        print("No new emails")
        return

    for msg in messages:
        msg_id = msg["id"]

        sender, subject, body = get_email_details(service, msg_id)

        print(f"\nFrom: {sender}")
        print(f"Subject: {subject}")

        if "noreply" in sender.lower() or "no-reply" in sender.lower():
            mark_as_read(service, msg_id)
            print("Ignored no-reply email")
            continue

        if EMAIL and EMAIL.lower() in sender.lower():
            mark_as_read(service, msg_id)
            print("Ignored self email")
            continue

        if not body.strip():
            mark_as_read(service, msg_id)
            print("Ignored empty email")
            continue

        body_lower = body.lower()
        if any(
            keyword in body_lower
            for keyword in [
                "unsubscribe",
                "opt out",
                "do not reply",
                "newsletter",
                "<html",
            ]
        ):
            mark_as_read(service, msg_id)
            print("Ignored promotional email")
            continue

        cleaned_body = clean_email(body)

        try:
            email = extract_email(sender)
            user_id = email
            history = get_conversation(user_id)
            result = process_message(
                user_id, cleaned_body, history=[], platform="gmail"
            )
            print(f"Processed message with intent: {result['type']}")

            if result["type"] == "file":
                send_file_email(service, sender, subject, result["file_path"])
                mark_as_read(service, msg_id)
                print("Sent file email")
                continue
            else:
                if not result["message"]:
                    mark_as_read(service, msg_id)
                    print("AI failed")
                    continue
                send_reply(service, sender, subject, result["message"])
                print("Sent text reply")
                mark_as_read(service, msg_id)
                print("Email processed and marked as read")
                time.sleep(1)

        except Exception as e:
            print("Error:", e)


def mark_as_read(service, msg_id):

    service.users().messages().modify(
        userId="me",
        id=msg_id,
        body={"removeLabelIds": ["UNREAD"]},
    ).execute()


def get_email_summary(limit=1):
    service = get_gmail_service()
    result = (
        service.users()
        .messages()
        .list(userId="me", labelIds=["INBOX"], maxResults=limit)
        .execute()
    )
    messages = result.get("messages", [])
    summaries = []
    if not messages:
        print("No emails found.")
        return summaries
    for msg in messages:
        msg_id = msg["id"]
        sender, subject, body = get_email_details(service, msg_id)
        summary = f"From: {sender}\nSubject: {subject}\nSnippet: {body[:100]}"
        summaries.append(summary)
    return "\n\n".join(summaries)


def start_email_listener():
    while True:
        print("\nChecking emails...")
        auto_reply()
        time.sleep(120)


def extract_email(sender):
    match = re.search(r"[\w\.-]+@[\w\.-]+", sender)
    return match.group(0) if match else sender
