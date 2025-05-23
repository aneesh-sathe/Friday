import ast
import random
import re
from time import sleep

import ollama
from duckduckgo_search import DDGS
from duckduckgo_search.exceptions import DuckDuckGoSearchException


def generate_query(model: str, keywords: list[str]) -> list[str] | None:
    try:
        response: ollama.ChatResponse = ollama.chat(
            model=model,
            messages=[
                {
                    "role": "user",
                    "content": f"""You are a stock research assistant that generates concise, high-quality search queries for a downstream search function.

                    Your primary objective is to prioritize the most relevant and timely information — including current news, financial reports, earnings announcements, regulatory changes, mergers and acquisitions, and other recent developments — related to the following keywords: {keywords}.

                    Return 5 specific and well-structured search queries that would yield the most up-to-date results.

                    Return type: a Python list of strings. Return ONLY the list. No explanation, no preamble, no formatting.""",
                },
            ],
        )
        content = response["message"]["content"]

        if "<think>" in content and "</think>" in content:
            content = re.sub(r"<think.*?</think>", "", content, flags=re.DOTALL)
        query_list = ast.literal_eval(content)
        return query_list
    except ollama.ResponseError as e:
        print("Error:", e.error)
        if e.status_code == 404:
            ollama.pull(model)


def generate_links(
    keywords: list[str], model: str = "qwen3:4b", max_results: int = 3
) -> tuple[list[str], list[str]]:
    links = []
    search_list = generate_query(model=model, keywords=keywords)

    if search_list:
        for query in search_list:
            try:
                search_result = DDGS().text(query, max_results=max_results)
                sleep(random.uniform(5, 10))  # instead of a fixed 5s
                print(search_result)
                for body in search_result:
                    links.append(body["href"])
            except DuckDuckGoSearchException as e:
                print(f"DuckDuckGoSearchException: {e}")
            except Exception as e:
                print(f"Unhandled Exception: {type(e).__name__} - {e}")
        urls = [url for url in links if not url.lower().endswith(".pdf")]
        # print(f"fetched {len(urls)} links ")
        return (urls, search_list)

    else:
        # print("failed to fetch results")
        raise SystemExit("stopping app: failed to fetch results")
