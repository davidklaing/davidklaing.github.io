from typing import List, Optional

from sitebuilder.library.author import Author
from sitebuilder.library.tag import Tag


class Book:

    def __init__(self, title: str, author1: Author, author2: Optional[Author], publication_year: int, tags: List[Tag], url = str):
        self.title = title
        self.author1 = author1
        self.author2 = author2
        self.publication_year = publication_year
        self.tags = tags
        self.url = url
    
    @property
    def authors_display(self):
        if not self.author2:
            return self.author1.surname
        else:
            return f'{self.author1.surname} & {self.author2.surname}'
    
    @property
    def title_display(self):
        if self.url:
            if self.url[0] == '/':
                id = self.url.strip('/')
                return f'<a id="{id}" class="internal-link" href="{self.url}">{self.title}</a> '
            else:
                return f'[{self.title}]({self.url})'
    
    @property
    def display(self):
        return f'{self.authors_display}, _{self.title_display}_ {self.publication_year}'
