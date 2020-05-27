import pandas as pd

library = pd.read_csv('library.csv')

class Shelf:

    def __init__(self, library, rating = None, period_of_my_life = None, genre = None, subgenre = None):
        self.shelf = library
        self.rating = rating
        self.period_of_my_life = period_of_my_life
        self.genre = genre
        self.subgenre = subgenre
        self.prune_shelf()
    
    def prune_shelf(self):
        if self.rating is not None:
            self.shelf = self.shelf[self.shelf['rating'] == self.rating]
        if self.period_of_my_life is not None:
            self.shelf = self.shelf[self.shelf['period_of_my_life'] == self.period_of_my_life]
        if self.genre is not None:
            self.shelf = self.shelf[self.shelf['genre'] == self.genre]
        if self.subgenre is not None:
            self.shelf = self.shelf[self.shelf['subgenres'].str.contains(self.subgenre)]
        self.shelf.sort_values(by='author_surname')
    
    def make_page(self):
        id, title = self.make_yaml_attributes()
        page = [
            '---\n',
            'layout: page\n',
            f'title: "{title}"\n',
            'published: true\n',
            f'permalink: /{id}/\n',
            'backlinks: \n',
            '---\n',
            '\n'
        ]
        for index, book in self.shelf.iterrows():
            string = f"* {book['author_surname']}, *{book['title']}* ({book['publication_year']})"
            if self.rating is None:
                if book['rating'] == 'Loved':
                    string += ' ★'
            page.append(string + '\n')
        return page
    
    def make_yaml_attributes(self):
        if self.rating is not None:
            return (
                f'bookshelf-{self.rating.lower().replace(" ", "-")}', 
                f'{self.rating}'
            )
        if self.period_of_my_life is not None:
            return (
                f'bookshelf-{self.period_of_my_life.lower()}', 
                f'{self.period_of_my_life}'
            )
        if self.genre is not None:
            return (
                f'bookshelf-{self.genre.lower()}', 
                f'{self.genre}'
            )
        if self.subgenre is not None:
            return (
                f'bookshelf-{self.subgenre.strip("{}").lower().replace(" ", "-").replace("&", "and")}', 
                f'{self.subgenre.strip("{}")}'
            )
        else:
            return (
                f'all-books', 
                f'All books'
            )

def write_page(filepath, content):
    """Write a page."""
    with open(filepath, 'w') as f:
        return f.write(content)


def make_rating_pages():
    for rating in ['Loved', 'Liked', 'Mixed Feelings', 'Disliked', 'Indifferent']:
        shelf = Shelf(library, rating=rating)
        id, title = shelf.make_yaml_attributes()
        page = shelf.make_page()
        write_page(filepath=f'pages/{id}.md', content=''.join(page))


def make_period_pages():
    for period in ['Childhood', 'Teens', '20s']:
        shelf = Shelf(library, period_of_my_life=period)
        id, title = shelf.make_yaml_attributes()
        page = shelf.make_page()
        write_page(filepath=f'pages/{id}.md', content=''.join(page))


def make_genre_pages():
    for genre in ['Fiction', 'Non-Fiction']:
        shelf = Shelf(library, genre=genre)
        id, title = shelf.make_yaml_attributes()
        page = shelf.make_page()
        write_page(filepath=f'pages/{id}.md', content=''.join(page))


def make_subgenre_pages():
    subgenres = [
        '{Biographies}',
        '{Business}',
        '{Comics}',
        '{Computer Science & Programming}',
        '{Economics}',
        '{Essays}',
        '{Fantasy}',
        '{Historical Fiction}',
        '{History}',
        '{Learning}',
        '{Literature}',
        '{Memoirs}',
        '{Parables}',
        '{Personal Finance}',
        '{Philosophy}', 
        '{Plays}',
        '{Psychology}', 
        '{Religion}',
        '{Science}', 
        '{Science-Fiction}',
        '{Self-Help}',
        '{Short Stories}',
        '{Statistics}',
        '{Westerns}',
        '{Writin}'
    ]
    for subgenre in subgenres:
        shelf = Shelf(library, subgenre=subgenre)
        id, title = shelf.make_yaml_attributes()
        page = shelf.make_page()
        write_page(filepath=f'pages/{id}.md', content=''.join(page))


def build_library():
    all_books = Shelf(library)
    page = all_books.make_page()
    write_page(filepath=f'pages/bookshelf-all-books.md', content=''.join(page))
    make_rating_pages()
    make_period_pages()
    make_genre_pages()
    make_subgenre_pages()


if __name__ == "__main__":
    build_library()

'(Science)'.strip('()')
