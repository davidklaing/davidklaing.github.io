from typing import List, Optional, Tuple

from sitebuilder.library.author import Author


class Book:

    def __init__(
        self, 
        title: str, 
        series_index: Optional[int],
        author1: Author, 
        author2: Optional[Author], 
        publication_year: int, 
        tags: List[str], 
        url = Optional[str]
    ):
        self.title = title
        self.series_index = series_index
        self.author1 = author1
        self.author2 = author2
        self.publication_year = publication_year
        self.tags = tags
        self.url = url

        self.publication_era, self.publication_era_title, self.publication_era_path = self.publication_era_info()
    

    @property
    def authors_display(self) -> str:
        if not self.author2:
            return self.author1.full_name
        else:
            return f'{self.author1.full_name} & {self.author2.full_name}'
    

    @property
    def title_display(self) -> str:
        if self.url:
            if self.url[0] == '/':
                id = self.url.strip('/')
                return f'<a id="{id}" class="internal-link" href="{self.url}">{self.title}</a>'
            else:
                return f'[{self.title}]({self.url})'
        return self.title
    

    @property
    def display(self) -> str:
        return f'{self.authors_display}, _{self.title_display}_ ({self.publication_year})'


    def publication_era_info(self) -> Tuple[str, str, str]:
        if self.publication_year < 1800:
            era = '<1800'
            title = f"Books I&#39;ve read that were published before 1800"
            path = 'published-before-1800'
            return (era, title, path)
        else:
            if self.publication_year < 1900:
                floor = 100
                append_s = True
            elif self.publication_year < 2000:
                floor = 10
                append_s = True
            else:
                floor = 1
                append_s = False
            era = str(self.publication_year - self.publication_year % floor)
            title = f"Books I&#39;ve read that were published in {era}"
            path = f'published-in-{era}'
            if append_s:
                title += 's'
                path += 's'
            return (era, title, path)