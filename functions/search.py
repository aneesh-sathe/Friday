import ast
import re
from time import sleep

import ollama
from duckduckgo_search import DDGS

keywords = ["Tata Motors", "2025", "2024"]


def generate_query(model: str, keywords: list[str]) -> list[str] | None:
    try:
        response: ollama.ChatResponse = ollama.chat(
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
        query_list = ast.literal_eval(content)
        return query_list
    except ollama.ResponseError as e:
        print("Error:", e.error)
        if e.status_code == 404:
            ollama.pull(model)


def generate_links(keywords: list[str], model: str, max_results: int):
    links = []
    search_list = generate_query(model=model, keywords=keywords)
    # print(search_list)
    if search_list:
        for query in search_list:
            search_result = DDGS().text(query, max_results=max_results)
            sleep(3)
            print(search_result)
            for body in search_result:
                links.append(body["href"])
        return links
    else:
        print("Unable to generate links")


if __name__ == "__main__":
    # print(search_web("zomato annual report 2024 site:https://www.screener.in/", 5))
    print(generate_links(keywords, "qwen3:4b", 2))
