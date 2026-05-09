import os

from dotenv import load_dotenv
from litellm import completion

load_dotenv()


MODEL = os.getenv("MODEL")
FAILSAFE_MODEL = os.getenv("FAILSAFE_MODEL")


def ask_model(messages, model):

    response = completion(
        model=model,
        messages=messages,
    )

    return response["choices"][0]["message"]["content"]


def generate_reply(user_message, system_prompt: str, history: list):

    message = []

    if system_prompt:
        message.append({"role": "system", "content": system_prompt})
    message.extend(history)
    message.append({"role": "user", "content": user_message})
    try:
        return ask_model(message, MODEL)
    except Exception as e:
        print(f"Error with primary model: {e}")
        try:
            return ask_model(message, FAILSAFE_MODEL)
        except Exception as e:
            print(f"Error with failsafe model: {e}")
            return "Sorry, something went wrong."
