import pandas as pd

library = pd.read_csv('library.csv')

class Shelf:

    def __init__(self, library, rating = None, period_of_my_life = None, tag = None):
        self.shelf = library
        self.rating = rating
        self.period_of_my_life = period_of_my_life
        self.tag = tag
        self.prune_shelf()
    
    def prune_shelf(self):
        if self.rating is not None:
            self.shelf = self.shelf[self.shelf['rating'] == self.rating]
        if self.period_of_my_life is not None:
            self.shelf = self.shelf[self.shelf['period_of_my_life'] == self.period_of_my_life]
        if self.tag is not None:
            self.shelf = self.shelf[self.shelf['tags'].str.contains(self.tag)]
        self.shelf.sort_values(by='creator_key')
    
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
            string = f"* {book['creator_key']}, *{book['title']}* ({book['publication_year']})"
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
                f'bookshelf-{self.period_of_my_life.lower().replace(" ", "-")}', 
                f'{self.period_of_my_life}'
            )
        if self.tag is not None:
            return (
                f'bookshelf-{self.tag.strip("{}").lower().replace(" ", "-").replace("&", "and")}', 
                f'{self.tag.strip("{}")}'
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
    for rating in ['Loved', 'Liked', 'Mixed feelings', 'Disliked', 'Indifferent']:
        shelf = Shelf(library, rating=rating)
        id, title = shelf.make_yaml_attributes()
        page = shelf.make_page()
        write_page(filepath=f'pages/{id}.md', content=''.join(page))


def make_period_pages():
    for period in ['Childhood', 'Teens', '20s', 'In the past year']:
        shelf = Shelf(library, period_of_my_life=period)
        id, title = shelf.make_yaml_attributes()
        page = shelf.make_page()
        write_page(filepath=f'pages/{id}.md', content=''.join(page))


def make_tag_pages():
    tags = [
        '{Biographies}',
        '{Business}',
        '{Comics}',
        '{Computer Science & Programming}',
        '{Economics}',
        '{Essays}',
        '{Fantasy}',
        '{Fiction}',
        '{Historical Fiction}',
        '{History}',
        '{Learning}',
        '{Literature}',
        '{Memoirs}',
        '{Non-Fiction}',
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
        '{Writing}'
    ]
    for tag in tags:
        shelf = Shelf(library, tag=tag)
        id, title = shelf.make_yaml_attributes()
        page = shelf.make_page()
        write_page(filepath=f'pages/{id}.md', content=''.join(page))


def build_library():
    all_books = Shelf(library)
    page = all_books.make_page()
    write_page(filepath=f'pages/bookshelf-all-books.md', content=''.join(page))
    make_rating_pages()
    make_period_pages()
    make_tag_pages()


if __name__ == "__main__":
    build_library()
