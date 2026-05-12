import re


def detect_intent(message: str):

    message = message.lower().strip()

    file_trigger_words = [
        "send",
        "give",
        "file",
        "document",
    ]

    is_file_request = any(word in message for word in file_trigger_words)

    if is_file_request:

        message = re.sub(r"[\w\.-]+@[\w\.-]+", "", message)

        cleaned = (
            message.replace("send me", "")
            .replace("send", "")
            .replace("give me", "")
            .replace("give", "")
            .replace("file", "")
            .replace("document", "")
            .replace("to", "")
            .strip()
        )

        parts = cleaned.split()

        extensions = {
            "jpg",
            "jpeg",
            "png",
            "pdf",
            "txt",
            "docx",
            "csv",
            "pptx",
        }

        if parts and parts[-1] in extensions:

            ext = parts[-1]

            filename = "_".join(parts[:-1])

            cleaned = f"{filename}.{ext}"

        return {
            "intent": "file",
            "file_name": cleaned,
        }

    if "market report" in message and "everyday" in message:

        return {"intent": "schedule_market_report"}

    market_summary_keywords = [
        "market summary",
        "stock market summary",
        "market update",
        "stock update",
        "market report",
        "how's market",
        "market today",
        "market performance",
        "daily market summary",
    ]

    if any(keyword in message for keyword in market_summary_keywords):

        return {"intent": "market_summary"}

    email_summary_keywords = [
        "summarize email",
        "summarize emails",
        "email summary",
        "mail summary",
        "summarize my inbox",
        "summarize inbox",
    ]

    if any(keyword in message for keyword in email_summary_keywords):

        return {"intent": "summarize_email"}

    web_keywords = [
        "latest",
        "today",
        "news",
        "current",
        "recent",
        "price",
        "weather",
        "web search",
        "search the web",
    ]

    if any(keyword in message for keyword in web_keywords):

        return {"intent": "web_search"}

    rag_keywords = [
        "who is",
        "tell me about",
        "what do you know about",
        "details about",
        "information about",
        "remember",
        "my",
        "mine",
        "favorite",
    ]

    if any(keyword in message for keyword in rag_keywords):

        return {"intent": "rag_query"}

    knowledge_patterns = [
        "my name is",
        "i work at",
        "i live in",
        "my favorite",
        "i like",
        "i am",
        "my",
    ]

    if any(pattern in message for pattern in knowledge_patterns):

        return {"intent": "store_knowledge"}

    return {"intent": "chat"}
