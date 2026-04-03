from pydantic import BaseModel


class CreateClient(BaseModel):

    name: str
    identification: str
    address: str
    email: str


class Client(CreateClient):

    id: int

    class Config:
        orm_mode = True