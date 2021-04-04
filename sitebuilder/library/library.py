from typing import List

from sitebuilder.library.author import Author
from sitebuilder.library.book import Book
from sitebuilder.library.reading import Reading
from sitebuilder.library.shelf import Shelf
from sitebuilder.library.tag import Tag


class Library:

    def __init__(self, authors: List[Author], books: List[Book], readings: List[Reading], tags: List[Tag]):
        self.authors = authors
        self.books = books
        self.readings = readings
        self.tags = tags

    
    def get_shelves_by_publicaton_date(self):
        shelves = {}
        for book in self.books:
            if not book.publication_era in shelves:
                shelves.update({
                    book.publication_era: {
                        'title': book.publication_era_title,
                        'path': book.publication_era_path,
                        'books': [book]
                    }
                })
            else:
                shelves[book.publication_era]['books'].append(book)
        return [Shelf(shelf['title'], shelf['path'], shelf['books']) for shelf in shelves]


    def get_shelves_by_read_date(self):
        shelves = {}
        for reading in self.readings:
            if not reading.year_title in shelves:
                shelves.update({
                    reading.year_title: {
                        'title': reading.year_title,
                        'path': reading.year_path,
                        'books': [reading.book]
                    }
                })
            else:
                shelves[reading.year_title]['books'].append(reading.book)
        return [Shelf(shelf['title'], shelf['path'], shelf['books']) for shelf in shelves]


    def get_shelves_by_genre(self):
        shelves = {tag.tag: {'title': tag.title, 'path': tag.path, 'books': []} for tag in self.tags}
        for book in self.books:
            for tag in book.tags:
                shelves[tag]['books'].append(book)
        return [Shelf(shelf['title'], shelf['path'], shelf['books']) for shelf in shelves]
