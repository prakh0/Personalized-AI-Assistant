import os
import re
from .search import find_file
from ..llm.provider import generate_reply
from .summary import summarize_email
from ..services.prompt import WHATSAPP_ASSISTANT_PROMPT, GMAIL_ASSISTANT_PROMPT
from ..services.stocks import get_market_summary
from app.rag.vector_store import store_document
from ..rag.pipeline import build_prompt


def process_message(user_id: str, user_msg: str, history: list, platform="whatsapp"):

    lower_msg = user_msg.lower()

    if "market report" in lower_msg and "everyday" in lower_msg:
        from app.services.scheduler import schedule_daily_report

        schedule_daily_report(user_id)
        return {"type": "text", "message": "Scheduled daily market report at 5 PM"}

    if "market summary" in lower_msg:
        print("MARKET SUMMARY REQUEST DETECTED")
        report = get_market_summary()
        return {"type": "text", "message": report}

    if "summarize email" in lower_msg:
        print("EMAIL SUMMARY REQUEST DETECTED")
        summary = summarize_email()
        return {"type": "text", "message": summary}
    email_match = re.search(r"[\w\.-]+@[\w\.-]+", user_msg)

    file_keywords = [
        "send",
        ".pdf",
        ".jpg",
        ".jpeg",
        ".png",
        ".txt",
        ".docx",
        ".csv",
        ".pptx",
    ]

    words = lower_msg.split()
    is_file_request = any(
        keyword in words or keyword in lower_msg for keyword in file_keywords
    )

    if is_file_request:
        cleaned = lower_msg.replace("send me", "").replace("send", "").strip()
        if email_match:
            cleaned = re.sub(r"[\w\.-]+@[\w\.-]+", "", cleaned)
            cleaned = cleaned.replace("to", "").strip()

        print("FILE REQUEST DETECTED")

        print(f"\nSearching for: {cleaned}")

        file_path = find_file(cleaned)

        if file_path:

            print(f"File found: {file_path}")

            if email_match:
                return {
                    "type": "email_file",
                    "file_path": file_path,
                    "file_name": os.path.basename(file_path),
                    "email": email_match.group(0),
                }

            return {
                "type": "file",
                "file_path": file_path,
                "file_name": os.path.basename(file_path),
            }

        print("File not found")

        return {"type": "text", "message": "Couldn't find that file"}

    print("CHAT REQUEST")

    if platform == "whatsapp":
        prompt = WHATSAPP_ASSISTANT_PROMPT

    else:
        prompt = GMAIL_ASSISTANT_PROMPT

    if platform == "whatsapp":
        try:
            if is_knowledge(user_msg):
                print("STORING KNOWLEDGE")

                store_document(
                    content=user_msg,
                    user_id=user_id,
                    source="knowledge",
                )
        except Exception as e:
            print("Error storing document:", e)

    if platform == "whatsapp" and should_use_rag(user_msg):
        print("RAG TRIGGERED")

        final_prompt = build_prompt(query=user_msg, memory=history, user_id=user_id)
    else:
        final_prompt = user_msg

    reply = generate_reply(final_prompt, prompt, history)

    if not reply:

        print("AI reply failed")

        return {"type": "text", "message": None}

    return {"type": "text", "message": reply}


def should_use_rag(msg: str) -> bool:
    keywords = ["what", "how", "explain", "tell", "info", "details", "who"]
    return any(k in msg.lower() for k in keywords)


def is_knowledge(msg: str) -> bool:
    msg = msg.lower().strip()

    if msg.endswith("?"):
        return False

    if len(msg.split()) < 5:
        return False

    return True
