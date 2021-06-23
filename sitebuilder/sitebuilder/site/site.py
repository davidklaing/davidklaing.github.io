from typing import Dict, List, Set

from bs4 import BeautifulSoup

from sitebuilder.site.front_matter import FrontMatter
from sitebuilder.site.page import Page
from sitebuilder.site.tag_dict import tag_dict


class Site:
    """A representation of a set of pages.

    @param pages: A list of Page instances.

    """

    def __init__(self, pages: List[Page]):
        self.pages = pages
        self.make_all_pages_page()
        self.make_tag_pages()
        self.titles_dict: Dict[str, str] = {page.permalink: page.title for page in self.pages}

    def make_all_pages_page(self):
        front_matter = FrontMatter(
            title = 'All pages by date',
            published = 'true',
            permalink = '/all-pages-by-date/'
        )
        all_pages_page = front_matter.create_front_matter()
        pages_with_dates = sorted(
            [page for page in self.pages if page.publication_date or page.last_updated],
            key=lambda page: (page.publication_date, page.title),
            reverse=True
        )
        pub_year_header = '2100'
        for page in pages_with_dates:
            permalink = page.permalink
            id = permalink.strip("/")
            title = page.title
            updated = f' (updated {page.last_updated})' if page.last_updated else ''
            pub_year = page.publication_date[0:4]
            pub_monthday = page.publication_date[5:]
            if pub_year < pub_year_header:
                pub_year_header = pub_year
                all_pages_page.append(f'\n## {pub_year_header}\n')
            all_pages_page.append(
                f'- {pub_monthday} — <a id="{id}" class="internal-link" href="{permalink}">{title}</a>{updated}\n'
            )
        self.pages.append(Page(page = all_pages_page, folder = 'pages'))

    def make_tag_pages(self):
        for tag, pretty_name in tag_dict.items():
            self.make_tag_page(tag, pretty_name)
    
    def make_tag_page(self, tag, pretty_name):
        self.pages = [page for page in self.pages if page.title != pretty_name]
        front_matter = FrontMatter(
            title=pretty_name,
            published='true',
            permalink=f'/{tag}/'
        )
        tag_page = front_matter.create_front_matter()
        relevant_pages = sorted(
            [page for page in self.pages if page.tags and tag in page.tags],
            key=lambda page: (page.publication_date, page.title),
            reverse=True
        )
        pub_year_header = '2100'
        for page in relevant_pages:
            permalink = page.permalink
            id = permalink.strip("/")
            title = page.title
            updated = f' (updated {page.last_updated})' if page.last_updated else ''
            pub_year = page.publication_date[0:4]
            pub_monthday = page.publication_date[5:]
            if pub_year < pub_year_header:
                pub_year_header = pub_year
                tag_page.append(f'\n## {pub_year_header}\n')
            tag_page.append(
                f'- {pub_monthday} — <a id="{id}" class="internal-link" href="{permalink}">{title}</a>{updated}\n'
            )
        self.pages.append(Page(page = tag_page, folder = 'pages/automatically-created'))

    def update_backlinks(self):
        """Update all the backlinks in the site."""
        for page in self.pages:
            page.backlinks = self.find_backlinks(this_page=page)
            page.write_backlinks()

    def find_backlinks(self, this_page: Page) -> Set[str]:
        """Find all backlinks for a given page."""
        backlinks = []
        for other_page in self.pages:
            if this_page.permalink != other_page.permalink:
                for link in other_page.forward_links:
                    soup = BeautifulSoup(link, 'html.parser')
                    if soup.find('a').get('href') == this_page.permalink:
                        backlinks.append(self.make_anchor_tag(permalink=other_page.permalink))
        return sorted(set(backlinks))
    
    def make_anchor_tag(self, permalink: str) -> str:
        """Make an anchor tag, given a page's permalink."""
        if permalink == '/':
            id = 'home'
        else:
            id = permalink.strip('/')
        title = self.titles_dict[permalink]
        if title[0] == '"':
            title = title[1:-1]
        return f'<a id="{id}" class="internal-link" href="{permalink}">{title}</a>'
    
    def write_pages(self):
        """Write the pages back to markdown."""
        for page in self.pages:
            if page.permalink == '/':
                self.write_page(
                    filepath=f'index.md', 
                    content=''.join(page.front_matter + page.content)
                )
            else:
                path = page.permalink.strip('/') + '.md'
                folder = page.folder
                self.write_page(
                    filepath=f'{folder}/{path}', 
                    content=''.join(page.front_matter + page.content)
                )
    
    @staticmethod
    def write_page(filepath: str, content: str):
        """Write a page."""
        with open(filepath, 'w') as f:
            return f.write(content)
