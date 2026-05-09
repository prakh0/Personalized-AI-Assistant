def detect_file_intent(message: str):

    message = message.lower().strip()

    trigger_words = [
        "send",
        "give",
        "file",
        "document",
    ]

    is_file_request = any(word in message for word in trigger_words)

    if not is_file_request:

        return {"intent": "chat", "file_name": None}

    cleaned = (
        message.replace("send me", "")
        .replace("send", "")
        .replace("give me", "")
        .replace("give", "")
        .replace("file", "")
        .replace("document", "")
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

    if parts[-1] in extensions:

        ext = parts[-1]

        filename = "_".join(parts[:-1])

        cleaned = f"{filename}.{ext}"

    else:

        cleaned = "_".join(parts)

    return {"intent": "file", "file_name": cleaned}
