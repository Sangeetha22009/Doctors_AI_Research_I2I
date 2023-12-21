from pydantic import BaseModel

class CategoryForSummarizer(BaseModel):
    category_for_summarizer: list[str]

class QuestFromSummarizedResult(BaseModel):
    quest_from_summarized_result: str
