from pydantic import BaseModel

# Define the request model for message input
class MessageRequest(BaseModel):
    chat_id: int
    message: str