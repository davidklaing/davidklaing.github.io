from typing import Dict, List, Set

from bs4 import BeautifulSoup

from sitebuilder.site.page import Page


class Site:
    """A representation of a set of pages.

    @param pages: A list of Page instances.

    """

    def __init__(self, pages: List[Page]):
        self.pages = pages
        self.make_site_history_page()
        self.titles_dict: Dict[str, str] = {page.permalink: page.title for page in self.pages}

    def make_site_history_page(self):
        self.pages = [page for page in self.pages if page.title != 'Site history']
        pages_with_dates = sorted(
            [page for page in self.pages if page.publication_date or page.last_updated],
            key=lambda page: (page.last_updated, page.publication_date),
            reverse=True
        )
        site_history_page = [
            '---\n',
            'layout: page\n',
            f'title: Site history\n',
            'published: true\n',
            f'permalink: /site-history/\n',
            'backlinks: \n',
            '---\n',
            '\n'
        ]
        for page in pages_with_dates:
            if page.last_updated:
                site_history_page.append(
                    f'* {page.last_updated} <a id="{page.permalink.strip("/")}" class="internal-link" href="{page.permalink}">{page.title}</a> (update)\n'
                )
            else:
                site_history_page.append(
                    f'* {page.publication_date} <a id="{page.permalink.strip("/")}" class="internal-link" href="{page.permalink}">{page.title}</a>\n'
                )
        self.pages.append(site_history_page)


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
                self.write_page(filepath=f'index.md', content=''.join(page.front_matter + page.content))
            else:
                path = page.permalink.strip('/') + '.md'
                folder = page.folder
                self.write_page(filepath=f'{folder}/{path}', content=''.join(page.front_matter + page.content))
    
    @staticmethod
    def write_page(filepath: str, content: str):
        """Write a page."""
        with open(filepath, 'w') as f:
            return f.write(content)
