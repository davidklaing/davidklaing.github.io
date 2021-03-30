from typing import List

from sitebuilder.library.author import Author
from sitebuilder.library.book import Book
from sitebuilder.library.reading import Reading


class Library:

    def __init__(self, authors: List[Author], books: List[Book], readings: List[Reading]):
        self.authors = authors
        self.books = books
        self.readings = readings
    
    