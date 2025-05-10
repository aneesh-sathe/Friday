import re

from duckduckgo_search import DDGS
from ollama import ChatResponse, chat

keywords = ["Tata Motors"]


def generate_query(model: str, keywords: list[str]):
    response: ChatResponse = chat(
        model=model,
        messages=[
            {
                "role": "user",
                "content": f"""You are a stock research assistant that generates concise, high-quality search queries for a downstream search function.

                Your primary objective is to prioritize the most relevant and timely information — including current news, financial reports, earnings announcements, regulatory changes, mergers and acquisitions, and other recent developments — related to the following keywords: {keywords}.

                Return 5 to 10 specific and well-structured search queries that would yield the most up-to-date results.

                Return type: a Python list of strings. Return ONLY the list. No explanation, no preamble, no formatting.""",
            },
        ],
    )
    content = response["message"]["content"]

    if "<think>" in content and "</think>" in content:
        content = re.sub(r"<think.*?</think>", "", content, flags=re.DOTALL)

    print(content)


def search_web(query: str, max_results: int):
    res = DDGS().text(query, max_results=max_results)
    links = [body["href"] for body in res]
    return links


if __name__ == "__main__":
    # print(search_web("zomato annual report 2024 site:https://www.screener.in/", 5))
    generate_query("qwen3:4b", keywords)
