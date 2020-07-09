import pandas as pd

def build_library():
    build_book_pages()
    build_album_pages()
    build_link_pages()
    build_podcast_pages()


def build_book_pages():
    library = pd.read_csv('books.csv', dtype=str)
    write_shelf_page(Shelf(library, media_type='Book'))
    make_shelf_pages(
        library=library,
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
    library = pd.read_csv('albums.csv', dtype=str)
    write_shelf_page(Shelf(library, media_type='Album'))
    make_shelf_pages(
        library=library,
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


def build_link_pages():
    library = pd.read_csv('links.csv', dtype=str)
    write_shelf_page(Shelf(library, media_type='Link'))
    make_shelf_pages(
        library=library,
        media_type='Link',
        tags=[
            '{Communication}',
            '{Goal-setting}',
            '{Epistemology}',
            '{Media}',
            '{Memetics}',
            '{Productivity}',
            '{Progress}',
            '{Research}',
            '{Self-improvement}',
            '{Skill development}',
            '{Strategy}',
            '{Sublime introductory lectures}',
            '{Systems}',
        ]
    )


def build_podcast_pages():
    library = pd.read_csv('podcasts.csv', dtype=str)
    write_shelf_page(Shelf(library, media_type='Podcast'))
    make_shelf_pages(library=library, media_type='Podcast')


def make_shelf_pages(library, media_type, ratings = [], periods_of_my_life = [], tags = []):
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
    with open(f'library/{id}.md', 'w') as f:
        return f.write(''.join(page))


class Shelf:

    def __init__(self, library, media_type, rating = None, period_of_my_life = None, tag = None):
        self.shelf = library.sort_values(by=['creator_key', 'publication_year', 'title'])
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
            f'title: {title}\n',
            'published: true\n',
            f'permalink: /{id}/\n',
            'backlinks: \n',
            '---\n',
            '\n'
        ]
        for index, item in self.shelf.iterrows():
            if self.media_type in ['Link', 'Book']:
                creator_string = f"{item['creator_key']}, "
            elif self.media_type == 'Album':
                creator_string = f"{item['creator']}, "
            elif self.media_type == 'Podcast':
                creator_string = ''
            if not pd.isnull(item['url']):
                title = item["title"]
                url = item['url']
                if url[0] == '/':
                    id = url.strip('/')
                    title_string = f'<a id="{id}" class="internal-link" href="{url}">{title}</a> '
                else:
                    title_string = f'[{title}]({url}) '
            else:
                title_string = f'{item["title"]} '
            if not pd.isnull(item['publication_year']):
                year_string = f'({item["publication_year"]})'
            else:
                year_string = ''
            string = f"* {creator_string}{title_string}{year_string}"
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
