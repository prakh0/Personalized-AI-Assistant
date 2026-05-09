from app.rag.embedding import embed
from app.rag.chucking import chunk_text
from app.db.postgres import conn


def is_valid_content(text: str) -> bool:
    text = text.strip()

    if len(text.split()) < 5:
        return False

    if "?" in text:
        return False

    return True


def store_document(text, source, user_id):
    print("STORE FUNCTION CALLED")

    if not is_valid_content(text):
        print("Skipping invalid content:", text)
        return

    chunks = chunk_text(text)
    print("CHUNKS:", chunks)

    cur = conn.cursor()

    for chunk in chunks:
        print("Processing chunk:", chunk)

        emb = embed(chunk)
        print("Embedding length:", len(emb))

        try:
            cur.execute(
                """
                INSERT INTO documents (content, embedding, source, user_id)
                VALUES (%s, %s, %s, %s)
            """,
                (chunk, list(emb), source, user_id),
            )

            print("Inserted chunk")

        except Exception as e:
            print("DB INSERT ERROR:", e)

    conn.commit()
    print("COMMIT DONE")
