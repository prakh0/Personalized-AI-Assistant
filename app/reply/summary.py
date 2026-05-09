from app.llm.provider import generate_reply
from ..services.prompt import SUMMARIZATION_PROMPT


def summarize_email():

    from app.communication.gmail import get_email_summary

    emails = get_email_summary()

    if not emails:

        return "No emails found."

    reply = generate_reply(emails, SUMMARIZATION_PROMPT, history=[])

    return reply
