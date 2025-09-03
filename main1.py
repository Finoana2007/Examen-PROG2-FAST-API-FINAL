from fastapi import FastAPI, HTTPException
from fastapi.responses import PlainTextResponse
from pydantic import BaseModel
from typing import List

app = FastAPI()

class Details(BaseModel):
    year: int
    genre: str

class Book(BaseModel):
    isbn: str
    title: str
    author: str
    details: Details

book_db: List[Book] = []

# a
@app.get("/health")
async def health():
    return PlainTextResponse("SERVICE UP", status_code=200)

# b
@app.post("/phones", status_code=201)
async def create_phone(book: Book):
    if any(b.isbn == book.isbn for b in book_db):
        raise HTTPException(status_code=400, detail="Book already exists")
    book_db.append(book)
    return {"message": "Book added", "book": book}

# c
@app.get("/books", response_model=List[Book])
async def get_books():
    return [book for book in book_db if book.details.year > 2000]

# d
@app.get("/books/{isbn}", response_model=Book)
async def get_book(isbn: str):
    found = next((book for book in book_db if book.isbn == isbn), None)
    if found:
        return found
    raise HTTPException(status_code=404, detail="Book not found")

# e BONUS
@app.put("/books/{isbn}/details", response_model=Book)
async def update_book_details(isbn: str, details: Details):
    for book in book_db:
        if book.isbn == isbn:
            book.details = details
            return book
    raise HTTPException(status_code=404, detail="Book not found")