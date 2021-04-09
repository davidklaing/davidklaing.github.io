from loguru import logger
import pandas as pd
from typing import List, Optional

from sitebuilder.exceptions import MissingAuthorException, MissingBookException
from sitebuilder.library.author import Author
from sitebuilder.library.book import Book
from sitebuilder.library.library import Library
from sitebuilder.library.reading import Reading


def make_library():
    authors_df = pd.read_csv('data/books/authors.csv').fillna('')
    books_df = pd.read_csv('data/books/books.csv').fillna('')
    readings_df = pd.read_csv('data/books/readings.csv').fillna('')

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
            tags=get_tags(book),
            url=book['url']
        ) for book in books_df.to_dict(orient='records')
    ]


def get_author(authors: List[Author], author_number: int, book_row: List) -> Optional[Author]:
    author_name = book_row[f'author{author_number}']
    if author_name:
        matching_authors = [author for author in authors if author.full_name == author_name]
        if not matching_authors:
            logger.error(f'Missing author {author_name}')
            raise MissingAuthorException
        return matching_authors[0]
    else:
        return ''


def get_tags(book_row: List) -> List[str]:
    return book_row['tags'].split(',')


def make_readings(books: List[Book], readings_df: pd.DataFrame) -> List[Reading]:
    return [
        Reading(
            book=get_book(books, reading),
            year=reading['year'],
            format=reading['format'],
            status=reading['status']
        ) for reading in readings_df.to_dict(orient='records')
    ]


def get_book(books: List[Book], reading) -> Book:
    reading_title = reading['title']
    matching_books = [book for book in books if book.title == reading['title']]
    if not matching_books:
        logger.error(f'Missing book {reading_title}')
        raise MissingBookException
    return matching_books[0]