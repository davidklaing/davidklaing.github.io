import pandas as pd
from typing import List

from sitebuilder.library.person import Person
from sitebuilder.library.book import Book
from sitebuilder.library.library import Library
from sitebuilder.library.reading import Reading


def make_library():
    authors_df = pd.read_csv('data/books/authors.csv', dtype=str)
    books_df = pd.read_csv('data/books/authors.csv', dtype=str)
    readings_df = pd.read_csv('data/books/readings.csv', dtype=str)

    authors = make_authors(authors_df)
    books = make_books(authors, books_df)
    readings = make_readings(books, readings_df)

    return Library(authors=authors, books=books, readings=readings)


def make_authors(authors_df: pd.DataFrame) -> List[Person]:
    return [
        Person(
            surname=author['surname'], 
            full_name=author['full_name'], 
            gender=author['gender'], 
            nationality=author['nationality']
        ) for author in authors_df
    ]


def make_books(authors: List[Person], books_df: pd.DataFrame) -> List[Book]:
    return [
        Book(
            title=book['title'],
            author1=[author for author in authors if author.full_name == book['author1']][0],
            author2=[author for author in authors if author.full_name == book['author2']][0],
            publication_year=book['publication_year'],
            tags=book['tags'],
            url=book['url']
        ) for book in books_df
    ]


def make_readings(books: List[Book], readings_df: pd.DataFrame) -> List[Reading]:
    return [
        Reading(
            book=[book for book in books if book.title == reading['title']][0],
            year=reading['year'],
            format=reading['format'],
            status=reading['status']
        ) for reading in readings_df
    ]