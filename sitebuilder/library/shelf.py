from typing import List

from sitebuilder.library.book import Book

class Shelf:

    def __init__(self, title: str, path: str, books: List[Book]):
        self.title = title
        self.path = path
        self.books = sorted(books, key=lambda book: book.display)
    
    def make_page(self):
        page = [
            '---\n',
            'layout: page\n',
            f'title: {self.title}\n',
            'published: true\n',
            f'permalink: /books-{self.path}/\n',
            'backlinks: \n',
            '---\n',
            '\n'
        ]
        for book in self.books:
            page.append(f'* {book.display} \n')
        with open(f'library/books-{self.path}.md', 'w') as f:
            return f.write(''.join(page))