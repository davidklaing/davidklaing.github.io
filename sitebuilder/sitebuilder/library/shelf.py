from typing import List

from sitebuilder.library.book import Book
from sitebuilder.site.front_matter import FrontMatter

class Shelf:

    def __init__(self, title: str, path: str, books: List[Book]):
        self.title = title
        self.path = path
        self.books = sorted(books, key=lambda book: book.display)
    
    def make_page(self):
        front_matter = FrontMatter(
            title=self.title,
            published='true',
            permalink=f'/books-{self.path}/'
        )
        page = front_matter.create_front_matter()
        for book in self.books:
            page.append(f'* {book.display} \n')
        with open(f'pages/library/books-{self.path}.md', 'w') as f:
            return f.write(''.join(page))