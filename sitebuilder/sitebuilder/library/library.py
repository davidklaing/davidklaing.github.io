from typing import List

from sitebuilder.library.author import Author
from sitebuilder.library.book import Book
from sitebuilder.library.reading import Reading
from sitebuilder.library.shelf import Shelf
from sitebuilder.library.tags import tags
from sitebuilder.site.front_matter import FrontMatter


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
        shelves = sorted(shelves.values(), key=lambda shelf: shelf['path'], reverse=True)
        return [
            Shelf(
                title=shelf['title'], 
                path=shelf['path'], 
                books=shelf['books'],
                all_readings=self.readings
            ) for shelf in shelves
        ]


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
        shelves = sorted(shelves.values(), key=lambda shelf: shelf['path'], reverse=True)
        return [
            Shelf(
                title=shelf['title'], 
                path=shelf['path'], 
                books=shelf['books'], 
                all_readings=self.readings
            ) 
            for shelf in shelves
        ]


    def get_shelves_by_tag(self):
        shelves = {
            tag: {
                'title': f'Books tagged &#39;{tag}&#39;', 
                'path': f'tagged-{tag}', 
                'books': []
            } for tag in tags
        }
        for book in self.books:
            for tag in book.tags:
                shelves[tag]['books'].append(book)
        shelves = sorted(shelves.values(), key=lambda shelf: (-len(shelf['books']), shelf['path']), reverse=False)
        return [
            Shelf(
                title=shelf['title'], 
                path=shelf['path'], 
                books=shelf['books'], 
                all_readings=self.readings
            ) 
            for shelf in shelves
        ]


    def make_shelf_pages(self):
        for shelf_category in [
            self.shelves_by_publicaton_date, 
            self.shelves_by_read_date, 
            self.shelves_by_tag
        ]:
            for shelf in shelf_category:
                shelf.make_page()
    
    def make_library_home_page(self):
        front_matter = FrontMatter(
            title='Books I&#39;ve read',
            permalink='/books-ive-read/', 
            published='true'
        )
        page = front_matter.create_front_matter()
        preface = "In the pages below, you can browse all the books I’ve read. They are organized in three ways: by when I read them, by when they were published, and by tag. If you have a recommendation based on what you see here, please send it my way!\n\n"
        when_i_read_it_header = '## By when I read them\n\n'
        when_i_read_it_table = self.make_shelf_category_list(shelf_category=self.shelves_by_read_date)
        when_it_was_published_header = '## By when they were published\n\n'
        when_it_was_published_table = self.make_shelf_category_list(shelf_category=self.shelves_by_publicaton_date)
        by_tag_header = '## By tag\n\n'
        by_tag_table = self.make_shelf_category_list(shelf_category=self.shelves_by_tag)
        for component in [
            preface,
            when_i_read_it_header,
            when_i_read_it_table,
            when_it_was_published_header,
            when_it_was_published_table,
            by_tag_header,
            by_tag_table
        ]:
            page.append(component)
        with open(f'pages/automatically-created/books-ive-read.md', 'w') as f:
            return f.write(''.join(page))
    
    @staticmethod
    def make_shelf_category_list(shelf_category: List[Shelf]):
        category_list = ''
        for shelf in shelf_category:
            path = shelf.path
            title = shelf.title
            n_books = len(shelf.books)
            line = f'* <a id="books-{path}" class="internal-link" href="/books-{path}/">{title}</a> ({n_books})\n'
            if 'tag' in shelf.path:
                if n_books >= 1:
                    category_list += line
            else:
                category_list += line
        category_list += '\n\n'
        return category_list