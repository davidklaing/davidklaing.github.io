from loguru import logger
import pandas as pd
from typing import List, Optional

from sitebuilder.exceptions import MissingAuthorException
from sitebuilder.library.author import Author
from sitebuilder.library.book import Book
from sitebuilder.library.library import Library
from sitebuilder.library.reading import Reading


def make_library():
    authors_df = pd.read_csv('data/books/authors.csv')
    books_df = pd.read_csv('data/books/books.csv')
    readings_df = pd.read_csv('data/books/readings.csv')

    authors = make_authors(authors_df)
    books = make_books(authors, books_df)
    readings = make_readings(books, readings_df)

    return Library(authors=authors, books=books, readings=readings)


def make_authors(authors_df: pd.DataFrame) -> List[Author]:
    return [
        Author(
            surname=author['surname'], 
            full_name=author['full_name'], 
            gender=author['gender'], 
            nationality=author['nationality']
        ) for author in authors_df.to_dict(orient='records')
    ]


def make_books(authors: List[Author], books_df: pd.DataFrame) -> List[Book]:
    return [
        Book(
            title=book['title'],
            author1=get_author(authors, 1, book),
            author2=get_author(authors, 2, book),
            publication_year=book['publication_year'],
            tags=book['tags'].split(','),
            url=book['url']
        ) for book in books_df.to_dict(orient='records')
    ]

def get_author(authors: List[Author], author_number: int, book_row: List) -> Optional[str]:
    author_name = book_row[f'author{author_number}']
    if isinstance(author_name, str):
        author = [author for author in authors if author.full_name == author_name]
        if not author:
            logger.error(f'Missing author {author_name}')
            raise MissingAuthorException
        else:
            return author[0]
    else:
        return None

def make_readings(books: List[Book], readings_df: pd.DataFrame) -> List[Reading]:
    return [
        Reading(
            book=[book for book in books if book.title == reading['title']][0],
            year=reading['year'],
            format=reading['format'],
            status=reading['status']
        ) for reading in readings_df.to_dict(orient='records')
    ]