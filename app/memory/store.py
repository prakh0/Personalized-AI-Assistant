user_sessions = {}
max_conversation_length = 10


def get_conversation(user_id):
    if user_id not in user_sessions:
        user_sessions[user_id] = []
    return user_sessions[user_id]


def add_to_conversation(user_id, role, content):
    user_conversation = get_conversation(user_id)
    user_conversation.append({"role": role, "content": content})
    if len(user_conversation) > max_conversation_length:
        user_conversation[:] = user_conversation[-max_conversation_length:]


def reset_conversation(user_id):
    if user_id in user_sessions:
        user_sessions[user_id] = []
        print(f"Conversation reset for user: {user_id}")


def has_history(user_id):
    return user_id in user_sessions and len(user_sessions[user_id]) > 0
