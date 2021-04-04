from sitebuilder.library.book import Book


class Reading:

    def __init__(self, book: Book, year: int, format: str, status: str):
        self.book = book
        self.year = year
        self.format = format
        self.status = status

        if self.year < 2010:
            self.year_title = f'Read before 2010'
            self.year_path = f'read-before-2010'
        else:
            self.year_title = f'Read in {self.year}'
            self.year_path = f'read-in-{self.year}'