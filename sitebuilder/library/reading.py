from sitebuilder.library.book import Book


class Reading:

    def __init__(self, book: Book, year: int, format: str, status: str):
        self.book = book
        self.year = year
        self.format = format
        self.status = status
