from typing import List

from sitebuilder.library.author import Author
from sitebuilder.library.book import Book
from sitebuilder.library.reading import Reading
from sitebuilder.library.shelf import Shelf
from sitebuilder.library.tag_dict import tag_dict


class Library:

    def __init__(self, authors: List[Author], books: List[Book], readings: List[Reading]):
        self.authors = authors
        self.books = books
        self.readings = readings

        self.shelves_by_publicaton_date = self.get_shelves_by_publicaton_date()
        self.shelves_by_read_date = self.get_shelves_by_read_date()
        self.shelves_by_tag = self.get_shelves_by_tag()


    def get_shelves_by_publicaton_date(self):
        shelves = {}
        for book in self.books:
            if not book.publication_era in shelves.keys():
                shelves.update({
                    book.publication_era: {
                        'title': book.publication_era_title,
                        'path': book.publication_era_path,
                        'books': [book]
                    }
                })
            else:
                shelves[book.publication_era]['books'].append(book)
        return [Shelf(title=shelf['title'], path=shelf['path'], books=shelf['books']) for shelf in shelves.values()]


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
        return [Shelf(shelf['title'], shelf['path'], shelf['books']) for shelf in shelves.values()]


    def get_shelves_by_tag(self):
        shelves = {tag: {'title': title, 'path': tag, 'books': []} for tag, title in tag_dict.items()}
        for book in self.books:
            for tag in book.tags:
                shelves[tag]['books'].append(book)
        return [Shelf(shelf['title'], shelf['path'], shelf['books']) for shelf in shelves.values()]


    def make_shelf_pages(self):
        for shelf_category in [self.shelves_by_publicaton_date, self.shelves_by_read_date, self.shelves_by_tag]:
            for shelf in shelf_category:
                shelf.make_page()