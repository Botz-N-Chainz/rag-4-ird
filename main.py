from fastapi import FastAPI
from RAG.graph import app as rag_app
import os
from dotenv import load_dotenv
from fastapi.middleware.cors import CORSMiddleware
from typing import Dict, List
from web_crawler_and_scraper.crawl_n_scrape import scrape_website

load_dotenv()
os.environ['LANGCHAIN_TRACING_V2'] = 'true'
os.environ['LANGCHAIN_API_KEY'] = os.getenv('LANGCHAIN_API_KEY')  
os.environ['OPENAI_API_KEY'] = os.getenv('OPENAI_API_KEY')

app = FastAPI()
chat_histories: Dict[str, List[str]] = {}

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)


@app.get("/")
async def test():
    from pprint import pprint

    config = {"configurable": {"thread_id": "1234"}}
    # Run
    inputs = {
        "question": "How to fill the income tax return?",
        # "chat_history": chat_histories.get(config["configurable"]["thread_id"], [])
    }

    for output in rag_app.stream(inputs, config=config):
        for key, value in output.items():
            # Node
            pprint(f"Node '{key}':")
            # Optional: print full state at each node
            pprint(value, indent=2, width=80, depth=None)
        pprint("\n---\n")

    # Final generation
    pprint(value["generation"])
    thread_id = config["configurable"]["thread_id"]
    if thread_id not in chat_histories:
        chat_histories[thread_id] = []
    chat_histories[thread_id].append(value["generation"])
    return value["generation"]

@app.post("/chat")
async def chat(request: dict):
    from pprint import pprint
    question = request.get("question")
    thread_id = request.get("thread_id")

    language = request.get("language", "en")

    language_prompt = ""
    if language == "si":
        language_prompt = "Answer in Sinhala, "
    elif language == "ta":
        language_prompt = "Answer in Tamil, "
    elif language == "en":
        language_prompt = "Answer in English, "

    print(language_prompt + question)

    inputs = {
        "question": language_prompt + question
    }

    config = {"configurable": {"thread_id": thread_id}}
    for output in rag_app.stream(inputs, config=config):
        for key, value in output.items():
            pprint(f"Node '{key}':")
            pprint(value, indent=2, width=80, depth=None)
        pprint("\n---\n")

    # Final generation
    pprint(value["generation"])
    return {"answer": value["generation"]}

@app.post("/scrape")
async def scrape(request: dict):
    try:
        url = request.get("url")
        page_limit = request.get("page_limit")
        scrape_website(url, page_limit)
        return {"status": "ok"}
    except Exception as e:
        return {"status": "error", "message": str(e)}
