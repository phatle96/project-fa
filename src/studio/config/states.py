from langgraph.graph import MessagesState
from langchain_core.documents import Document
from typing_extensions import List, Optional

class MainState(MessagesState):
    summary: str
    context: List[Document]
    tool_calls_log: List[dict]
    current_tool_calls: List[dict]
    last_summarized_count: int
    processed_images: Optional[list[str]]
    image_descriptions: Optional[dict[str, str]]