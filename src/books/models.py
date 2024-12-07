from sqlmodel import SQLModel
from datetime import datetime
import uuid
class Book(SQLModel,table=True):
    uid: uuid.UUID
    title: str
    author  : str
    publisher: str
    published_date: str
    page_count: int
    language:str
    created_at:datetime
    updated_at:datetime

