import litellm


def embed(text: str):
    try:
        text = text.strip().lower()
        response = litellm.embedding(model="mistral/mistral-embed", input=text)
        return response["data"][0]["embedding"]
    except Exception as e:
        print(f"Error occurred while embedding text: {e}")
        return None
