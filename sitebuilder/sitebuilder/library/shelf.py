from typing import List

from sitebuilder.library.book import Book
from sitebuilder.library.reading import Reading
from sitebuilder.site.front_matter import FrontMatter

class Shelf:

    def __init__(self, title: str, path: str, books: List[Book], all_readings: List[Reading]):
        self.title = title
        self.path = path
        self.books = sorted(books, key=lambda book: (book.author1.surname, book.publication_year))
        self.all_readings = all_readings
    
    def books_with_given_status(self, status):
        all_books_with_given_status = {reading.book for reading in self.all_readings if reading.status == status}
        return [book for book in self.books if book in all_books_with_given_status]
    
    def make_page(self):
        front_matter = FrontMatter(
            title=self.title,
            published='true',
            permalink=f'/books-{self.path}/'
        )
        page = front_matter.create_front_matter()
        books_by_status = {
            status: self.books_with_given_status(status)
            for status in ['Finished', 'Skimmed, sampled from, or abandoned']
        }
        for status in books_by_status:
            if books_by_status[status]:
                page.append(f'\n\n## {status} \n')
                for book in books_by_status[status]:
                    page.append(f'* {book.display} \n')
        with open(f'pages/library/books-{self.path}.md', 'w') as f:
            return f.write(''.join(page))