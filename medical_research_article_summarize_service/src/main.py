from fastapi import FastAPI
from src.ScrapData1 import query_indexed_data, fetch_papers_for_categories
import logging
from fastapi.middleware.cors import CORSMiddleware
import src.scrape_summarizer_class as cls_summarize

app =  FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def test_endpoint():
    return "test result"

@app.post("/summarize")
def get_summarized_result(summarizer_categories: cls_summarize.CategoryForSummarizer):
    try:
        # response = query_indexed_data(query_for_summarizer)
        # print(summarizer_categories)
        response = fetch_papers_for_categories(summarizer_categories.category_for_summarizer)
        # print(f"\n Formatted response in main.py, {response}")
        summarized_result = f"{response}"
        # print(summarized_result)
        return {summarized_result}
        
    except Exception as e:
        logging.error(f"Exception occurred {e}")

@app.post("/query_reponse")
def get_query_reponse_summarized_data(query_for_summarizer: cls_summarize.QuestFromSummarizedResult):
    try:
        response = query_indexed_data(query_for_summarizer.quest_from_summarized_result)
        # print(f"\n Formatted response in main.py, {response}")
        summarized_result = f"{response}"
        # print(summarized_result)
        return {summarized_result}
        
    except Exception as e:
        logging.error(f"Exception occurred {e}")

