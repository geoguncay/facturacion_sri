from pydantic import BaseModel


class CreateClient(BaseModel):

    name: str
    client_id: str
    address: str
    email: str


class Client(CreateClient):

    id: int

    class Config:
        from_attributes = True
