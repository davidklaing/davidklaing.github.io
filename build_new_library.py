from typing import List, Optional

import pandas as pd


class Author:

    def __init__(self, surname: str, full_name: str, gender: str, nationality: str):
        self.surname = surname
        self.full_name = full_name
        self.gender = gender
        self.nationality = nationality


class Book:

    def __init__(self, title: str, author1: Author, author2: Optional[Author], publication_year: int, tags: List[str], url = str):
        self.title = title
        self.author1 = author1
        self.author2 = author2
        self.publication_year = publication_year
        self.tags = tags
        self.url = url
    
    @property
    def authors_display(self):
        if not self.author2:
            return self.author1.surname
        else:
            return f'{self.author1.surname} & {self.author2.surname}'
    
    @property
    def title_display(self):
        if self.url:
            if self.url[0] == '/':
                id = self.url.strip('/')
                return f'<a id="{id}" class="internal-link" href="{self.url}">{self.title}</a> '
            else:
                return f'[{self.title}]({self.url})'
    
    @property
    def display(self):
        return f'{self.authors_display}, _{self.title_display}_ {self.publication_year}'


class Reading:

    def __init__(self, book: Book, year: int, format: str, status: str):
        self.book = book
        self.year = year
        self.format = format
        self.status = status


class Shelf:

    def __init__(self, title: str, path: str, books: List[Book]):
        self.title = title
        self.path = path
        self.books = books
    
    def make_page(self):
        page = [
            '---\n',
            'layout: page\n',
            f'title: {self.title}\n',
            'published: true\n',
            f'permalink: /{self.path}/\n',
            'backlinks: \n',
            '---\n',
            '\n'
        ]
        for book in self.books:
            page.append(f'* {book.display} \n')
        return page


class Library:

    def __init__(self, authors: List[Author], books: List[Book], readings: List[Reading]):
        self.authors = authors
        self.books = books
        self.readings = readings

def make_library():
    authors_df = pd.read_csv('data/books/authors.csv', dtype=str)
    books_df = pd.read_csv('data/books/authors.csv', dtype=str)
    readings_df = pd.read_csv('data/books/readings.csv', dtype=str)

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
        ) for author in authors_df
    ]

def make_books(authors: List[Author], books_df: pd.DataFrame) -> List[Book]:
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