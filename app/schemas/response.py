from pydantic import BaseModel

class QueryResponse(BaseModel):
    response: str
    session_id: str