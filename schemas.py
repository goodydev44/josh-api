from pydantic import BaseModel

class Data(BaseModel):
    name: str
    phone: str
    message: str

    class Config():
        from_attributes = True

class ShowData(Data):
    id: int
    name: str
    phone: str
    message: str

    class Config():
        from_attributes = True