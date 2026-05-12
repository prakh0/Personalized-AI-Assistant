from tavily import TavilyClient
from dotenv import load_dotenv

import os

load_dotenv()

client = TavilyClient(api_key=os.getenv("TAVILY_API_KEY"))


def search_web(query: str, max_results: int = 5):

    try:
        response = client.search(
            query=query,
            max_results=max_results,
            search_depth="advanced",
        )

        formatted = []

        for r in response.get("results", []):

            formatted.append(
                {
                    "title": r.get("title", ""),
                    "url": r.get("url", ""),
                    "content": r.get("content", ""),
                }
            )

        return formatted

    except Exception as e:
        print("WEB SEARCH ERROR:", e)
        return []
