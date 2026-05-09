import os
from dotenv import load_dotenv
from fastapi import FastAPI, Request
from fastapi.responses import Response, FileResponse
import requests
import logging

from app.reply.search import get_full_path, get_relative_path
from app.reply.chat import process_message
from app.communication.gmail import send_file_email, get_gmail_service
from ..memory.store import add_to_conversation, reset_conversation, get_conversation

app = FastAPI()

logging.basicConfig(level=logging.INFO)

load_dotenv()

VERIFY_TOKEN = os.getenv("VERIFY_TOKEN")
ACCESS_TOKEN = os.getenv("ACCESS_TOKEN")
PHONE_NUMBER_ID = os.getenv("PHONE_NUMBER_ID")
BASE_URL = os.getenv("BASE_URL")


@app.get("/webhook")
async def verify_webhook(request: Request):
    token = request.query_params.get("hub.verify_token")
    challenge = request.query_params.get("hub.challenge")

    if token == VERIFY_TOKEN:
        return Response(content=challenge, media_type="text/plain")

    return Response(content="Verification failed", status_code=403)


def send_whatsapp_message(to, message):
    url = f"https://graph.facebook.com/v18.0/{PHONE_NUMBER_ID}/messages"

    headers = {
        "Authorization": f"Bearer {ACCESS_TOKEN}",
        "Content-Type": "application/json",
    }

    data = {
        "messaging_product": "whatsapp",
        "to": to,
        "text": {"body": message},
    }

    res = requests.post(url, headers=headers, json=data)

    print("TEXT STATUS:", res.status_code)
    print("TEXT RESPONSE:", res.text)


def send_whatsapp_document(to, file_url, filename):
    url = f"https://graph.facebook.com/v18.0/{PHONE_NUMBER_ID}/messages"

    headers = {
        "Authorization": f"Bearer {ACCESS_TOKEN}",
        "Content-Type": "application/json",
    }

    data = {
        "messaging_product": "whatsapp",
        "to": to,
        "type": "document",
        "document": {
            "link": file_url,
            "filename": filename,
        },
    }

    res = requests.post(url, headers=headers, json=data)

    print("FILE STATUS:", res.status_code)
    print("FILE RESPONSE:", res.text)


@app.get("/files")
def serve_file(path: str):
    full_path = get_full_path(path)
    return FileResponse(full_path)


@app.get("/")
def home():
    return {"status": "WhatsApp AI Agent is running"}


@app.post("/webhook")
async def whatsapp_webhook(request: Request):
    try:
        data = await request.json()

        entry = data.get("entry", [{}])[0]
        changes = entry.get("changes", [{}])[0]
        value = changes.get("value", {})

        messages = value.get("messages")

        if not messages:
            logging.info("No message found")
            return {"status": "ignored"}

        message = messages[0]

        if "text" not in message:
            return {"status": "ignored"}

        user_msg = message["text"]["body"]
        user_id = message["from"]

        logging.info(f"Message: {user_msg}")

        if user_msg.lower() in ["reset", "clear"]:
            reset_conversation(user_id)
            send_whatsapp_message(user_id, "Conversation reset")
            return {"status": "ok"}

        add_to_conversation(user_id, "user", user_msg)

        history = get_conversation(user_id)
        print("BEFORE HISTORY:", get_conversation(user_id))

        result = process_message(user_id, user_msg, history, platform="whatsapp")
        print("AFTER HISTORY:", get_conversation(user_id))

        if result["type"] == "file":
            relative_path = get_relative_path(result["file_path"])
            file_url = f"{BASE_URL}/files?path={relative_path}"
            send_whatsapp_document(user_id, file_url, result["file_name"])
            add_to_conversation(
                user_id,
                "assistant",
                f"Sent file: {result['file_name']} (URL: {file_url})",
            )

        elif result["type"] == "email_file":
            send_file_email(
                service=get_gmail_service(),
                to=result["email"],
                subject=f"File: {result['file_name']}",
                file_path=result["file_path"],
            )
            send_whatsapp_message(
                user_id, f"Sent {result['file_name']} to {result['email']}"
            )
            add_to_conversation(
                user_id,
                "assistant",
                f"Sent file: {result['file_name']} (URL: {file_url})",
            )
        else:
            if not result["message"]:
                send_whatsapp_message(
                    user_id, "Sorry, I couldn't generate a reply. Please try again."
                )
                return {"status": "error"}
            send_whatsapp_message(user_id, result["message"])
            if (
                result["message"]
                and "don't have enough information" not in result["message"].lower()
            ):
                add_to_conversation(user_id, "assistant", result["message"])
        return {"status": "ok"}
    except Exception as e:
        logging.error(f"Error processing message: {e}")
        return {"status": "error", "message": str(e)}
