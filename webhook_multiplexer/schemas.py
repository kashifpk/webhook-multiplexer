from pydantic import BaseModel


class CreateForwardRequest(BaseModel):

    incoming: str
    outgoing: str
