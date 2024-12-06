from fastapi import FastAPI,Header,status
from fastapi.exceptions import HTTPException
from typing import Optional,List
from pydantic import BaseModel

app = FastAPI()

books=[
    {
      "id": 1,
      "title": "The Catcher in the Rye",
      "author": "J.D. Salinger",
      "publisher": "Little, Brown and Company",
      "published_date": "1951-07-16",
      "page_count": 214,
      "language": "English"
    },
    {
      "id": 2,
      "title": "To Kill a Mockingbird",
      "author": "Harper Lee",
      "publisher": "J.B. Lippincott & Co.",
      "published_date": "1960-07-11",
      "page_count": 281,
      "language": "English"
    },
    {
      "id": 3,
      "title": "1984",
      "author": "George Orwell",
      "publisher": "Secker & Warburg",
      "published_date": "1949-06-08",
      "page_count": 328,
      "language": "English"
    },
    {
      "id": 4,
      "title": "One Hundred Years of Solitude",
      "author": "Gabriel García Márquez",
      "publisher": "Harper & Row",
      "published_date": "1970-02-05",
      "page_count": 417,
      "language": "Spanish"
    },
    {
      "id": 5,
      "title": "The Great Gatsby",
      "author": "F. Scott Fitzgerald",
      "publisher": "Charles Scribner's Sons",
      "published_date": "1925-04-10",
      "page_count": 180,
      "language": "English"
    }
  ]

class Book(BaseModel):
    id: int
    title: str
    author  : str
    publisher: str
    published_date: str
    page_count: int
    language:str

class BookUpdateModel(BaseModel):
    title: str
    author  : str
    publisher: str
    page_count: int
    language:str

@app.get("/")
async def read_root():
    return {"message": "Hello World"}

@app.get("/greet")
async def greet_name(name: Optional[str]="User",age:int=0)->dict:
    return {"message": f"Hello {name}","age":age}


@app.get("/get_headers",status_code=status.HTTP_201_CREATED)
async def get_headers(
        accept:str=Header(None),
        content_type:str=Header(None),
        user_agent:str=Header(None),
        host:str=Header(None)
):
    request_headers={}
    request_headers['Accept']=accept
    request_headers['Content-Type']=content_type
    request_headers["User-Agent"]=user_agent
    request_headers["Host"]=host
    return request_headers


@app.get("/books",response_model=List[Book])
async def get_all_books():
    return books

@app.post("/books",status_code=201)
async def create_a_book(book_data:Book)->dict:
    new_book=book_data.model_dump()
    books.append(new_book)
    return new_book

@app.get("/book/{book_id}")
async def get_book(book_id: int)->dict:
    for book in books:
        if book["id"]==book_id:
            return book
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="Book not found")

@app.patch("/book/{book_id}")
async def update_book(book_id: int,book_update_data:BookUpdateModel)->dict:
    for book in books:
        if book["id"]==book_id:
            book["title"]=book_update_data.title
            book["author"]=book_update_data.author
            book["publisher"]=book_update_data.publisher
            book["page_count"]=book_update_data.page_count
            book["language"]=book_update_data.language
            return book
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="Book not found")

@app.delete("/book/{book_id}",status_code=status.HTTP_204_NO_CONTENT)
async def delete_book(book_id: int)->dict:
    for book in books:
        if book["id"]==book_id:
            books.remove(book)
            return {"message":"Book deleted successfully"}
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="Book not found")
