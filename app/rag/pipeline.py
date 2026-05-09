from app.rag.retrieve import retrieve
from app.services.prompt import RAG_PROMPT


def build_prompt(query, memory, user_id):
    context = retrieve(query, user_id)

    print("\n===== RAG CONTEXT =====")
    print(context)
    print("=======================\n")

    if not context:
        return query

    context_text = "\n".join(context[:6])

    return RAG_PROMPT.format(context=context_text, query=query)
