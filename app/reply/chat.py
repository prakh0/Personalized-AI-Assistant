import os
import re
from .search import find_file
from .detect_intension import detect_intent
from ..llm.model import generate_reply
from .summary import summarize_email
from ..services.prompt import WHATSAPP_ASSISTANT_PROMPT, GMAIL_ASSISTANT_PROMPT
from ..services.stocks import get_market_summary
from app.rag.vector_store import store_document
from ..rag.pipeline import build_prompt
from ..web_search.web_search_format import build_web_prompt


def process_message(user_id: str, user_msg: str, history: list, platform="whatsapp"):

    intent_data = detect_intent(user_msg)
    intent = intent_data["intent"]

    if intent == "schedule_market_report":

        from app.services.scheduler import schedule_daily_report

        schedule_daily_report(user_id)

        return {
            "type": "text",
            "message": "Scheduled daily market report at 5 PM",
        }

    if intent == "market_summary":

        print("MARKET SUMMARY REQUEST DETECTED")

        report = get_market_summary()

        return {
            "type": "text",
            "message": report,
        }

    if intent == "summarize_email":

        print("EMAIL SUMMARY REQUEST DETECTED")

        summary = summarize_email()

        return {
            "type": "text",
            "message": summary,
        }

    email_match = re.search(r"[\w\.-]+@[\w\.-]+", user_msg)

    intent_data = detect_intent(user_msg)

    if intent_data["intent"] == "file":

        cleaned = intent_data["file_name"]

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

        return {
            "type": "text",
            "message": "Couldn't find that file",
        }

    print("CHAT REQUEST")

    if platform == "whatsapp":
        prompt = WHATSAPP_ASSISTANT_PROMPT

    else:
        prompt = GMAIL_ASSISTANT_PROMPT

    if platform == "whatsapp" and intent == "store_knowledge":
        try:
            print("STORING KNOWLEDGE")
            store_document(
                content=user_msg,
                user_id=user_id,
                source="knowledge",
            )
        except Exception as e:
            print("Error storing document:", e)

    if platform == "whatsapp" and intent == "web_search":

        print("WEB SEARCH INTENT DETECTED")

        final_prompt = build_web_prompt(user_msg)

        if not final_prompt:
            return {
                "type": "text",
                "message": "Couldn't find any relevant information on the web.",
            }
        reply = generate_reply(final_prompt, "", history)
        if not reply:
            return {
                "type": "text",
                "message": "Web search failed to generate a reply.",
            }
        return {
            "type": "text",
            "message": reply,
        }

    if platform == "whatsapp" and intent == "rag":
        print("RAG TRIGGERED")

        final_prompt = build_prompt(query=user_msg, memory=history, user_id=user_id)
    else:
        final_prompt = user_msg

    reply = generate_reply(final_prompt, prompt, history)

    if not reply:

        print("AI reply failed")

        return {"type": "text", "message": None}

    return {"type": "text", "message": reply}
