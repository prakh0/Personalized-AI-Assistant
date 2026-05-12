from app.services.websearch import search_web
from app.services.prompt import web_search_prompt


def build_web_prompt(query: str):

    results = search_web(query)

    print("\n===== WEB SEARCH RESULTS =====")
    print(results)
    print("==============================\n")

    if not results:
        return None

    formatted_results = "\n\n".join(
        [
            f"Title: {r['title']}\nURL: {r['url']}\nContent: {r['content']}"
            for r in results
        ]
    )

    return web_search_prompt.format(
        web_results=formatted_results,
        query=query,
    )
