import pandas as pd

library = pd.read_csv('library.csv')

def build_library():
    build_book_pages()
    build_album_pages()


def build_book_pages():
    write_shelf_page(Shelf(library, media_type='Book'))
    make_shelf_pages(
        media_type='Book',
        ratings=['Loved', 'Liked', 'Mixed feelings', 'Disliked', 'Indifferent'],
        periods_of_my_life=['Childhood', 'Teens', '20s', 'In the past year'],
        tags=[
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
    )


def build_album_pages():
    write_shelf_page(Shelf(library, media_type='Album'))
    make_shelf_pages(
        media_type='Album',
        periods_of_my_life=['Childhood', 'Teens', '20s', 'In the past year'],
        tags=[
            '{Alternative}',
            '{Bluegrass}',
            '{Christmas}',
            '{Classical}',
            '{Country}',
            '{Electronic}',
            '{Folk}',
            '{Funk}',
            '{Jazz}',
            '{Live}',
            '{Musicals}',
            '{Pop}',
            '{R & B}', 
            '{Rap}',
            '{Rock}'
        ]
    )


def make_shelf_pages(media_type, ratings = [], periods_of_my_life = [], tags = []):
    for rating in ratings:
        write_shelf_page(Shelf(library, media_type=media_type, rating=rating))
    for period_of_my_life in periods_of_my_life:
        write_shelf_page(Shelf(library, media_type=media_type, period_of_my_life=period_of_my_life))
    for tag in tags:
        write_shelf_page(Shelf(library, media_type=media_type, tag=tag))


def write_shelf_page(shelf):
    """Write a shelf page."""
    id, title = shelf.make_yaml_attributes()
    page = shelf.make_page()
    with open(f'pages/{id}.md', 'w') as f:
        return f.write(''.join(page))


class Shelf:

    def __init__(self, library, media_type, rating = None, period_of_my_life = None, tag = None):
        self.shelf = library.sort_values(by='creator_key')
        self.media_type = media_type
        self.rating = rating
        self.period_of_my_life = period_of_my_life
        self.tag = tag
        self.prune_shelf()
    
    def prune_shelf(self):
        self.shelf = self.shelf[self.shelf['media_type'] == self.media_type]
        if self.rating is not None:
            self.shelf = self.shelf[self.shelf['rating'] == self.rating]
        if self.period_of_my_life is not None:
            self.shelf = self.shelf[self.shelf['period_of_my_life'] == self.period_of_my_life]
        if self.tag is not None:
            self.shelf = self.shelf[self.shelf['tags'].str.contains(self.tag)]
    
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
        if self.media_type == 'Book':
            creator_indicated_by = 'creator_key'
        elif self.media_type == 'Album':
            creator_indicated_by = 'creator'
        for index, item in self.shelf.iterrows():
            string = f"* {item[creator_indicated_by]}, *{item['title']}* ({item['publication_year']})"
            if self.rating is None and self.media_type == 'Book':
                if item['rating'] == 'Loved':
                    string += ' ★'
            page.append(string + '\n')
        return page
    
    def make_yaml_attributes(self):
        if self.rating is not None:
            return (
                f'{self.media_type.lower()}s-{self.rating.lower().replace(" ", "-")}', 
                f'{self.rating}'
            )
        if self.period_of_my_life is not None:
            return (
                f'{self.media_type.lower()}s-{self.period_of_my_life.lower().replace(" ", "-")}', 
                f'{self.period_of_my_life}'
            )
        if self.tag is not None:
            return (
                f'{self.media_type.lower()}s-{self.tag.strip("{}").lower().replace(" ", "-").replace("&", "and")}', 
                f'{self.tag.strip("{}")}'
            )
        else:
            return (
                f'all-{self.media_type.lower()}s', 
                f'All {self.media_type.lower()}s'
            )


if __name__ == "__main__":
    build_library()
