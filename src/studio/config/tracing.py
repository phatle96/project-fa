from langfuse import Langfuse
from langfuse.langchain import CallbackHandler

langfuse = Langfuse(
  secret_key="sk-lf-324ccbab-33ff-4e74-a6b1-f792dd0ad3fc",
  public_key="pk-lf-8e901dc4-2eab-4997-bf5d-4c959902c955",
  host="http://localhost:3000"
)


langfuse_handler = CallbackHandler()
