from app.rag.embedding import embed
from app.db.postgres import conn


def to_pgvector(vec):
    return "[" + ",".join(map(str, vec)) + "]"


def retrieve(query, user_id, k=3):
    emb = embed(query)
    emb_str = to_pgvector(emb)

    cur = conn.cursor()

    cur.execute(
        """
        SELECT content, embedding <-> %s::vector AS distance
        FROM documents
        WHERE user_id = %s
        AND source = 'knowledge'
        ORDER BY embedding <-> %s::vector
        LIMIT %s;
        """,
        (emb_str, user_id, emb_str, k),
    )

    rows = cur.fetchall()

    results = []

    for content, distance in rows:
        print("DISTANCE:", distance)
        if distance < 1.0:
            results.append(content)

    print("RAG CONTEXT:", results)
    print("QUERY USER_ID:", user_id)

    return results
