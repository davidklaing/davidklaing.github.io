from typing import Dict, List, Set

from bs4 import BeautifulSoup

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
        self.pages = [page for page in self.pages if page.title != 'All pages by date']
        pages_with_dates = sorted(
            [page for page in self.pages if page.publication_date or page.last_updated],
            key=lambda page: (page.publication_date, page.title),
            reverse=True
        )
        all_pages_page = [
            '---\n',
            'layout: page\n',
            f'title: All pages by date\n',
            'published: true\n',
            f'permalink: /all-pages-by-date/\n',
            'backlinks: \n',
            '---\n',
            '\n'
        ]
        pub_year = '2070'
        for page in pages_with_dates:
            updated = f' (updated {page.last_updated})' if page.last_updated else ''
            pub_date = page.publication_date
            if pub_date[0:4] < pub_year:
                pub_year = pub_date[0:4]
                all_pages_page.append(f'\n## {pub_year}\n')
            pub_monthday = pub_date[5:]
            id = page.permalink.strip("/")
            permalink = page.permalink
            title = page.title
            all_pages_page.append(
                f'- {pub_monthday} — <a id="{id}" class="internal-link" href="{permalink}">{title}</a>{updated}\n'
            )
        self.pages.append(Page(page = all_pages_page, folder = 'pages'))

    def make_tag_pages(self):
        for tag, pretty_name in tag_dict.items():
            self.make_tag_page(tag, pretty_name)
    
    def make_tag_page(self, tag, pretty_name):
        self.pages = [page for page in self.pages if page.title != pretty_name]
        tag_page = [
            '---\n',
            'layout: page\n',
            f'title: {pretty_name}\n',
            'published: true\n',
            f'permalink: /{tag}/\n',
            'backlinks: \n',
            '---\n',
            '\n'
        ]
        if tag == 'meta':
            relevant_pages = sorted(
                [page for page in self.pages if page.tags and tag in page.tags],
                key=lambda page: page.title,
                reverse=False
            )
            for page in relevant_pages:
                tag_page.append(
                    f'<a id="{page.permalink.strip("/")}" class="internal-link" href="{page.permalink}">{page.title}</a>\n\n'
                )
        else:
            relevant_pages = sorted(
                [page for page in self.pages if page.tags and tag in page.tags],
                key=lambda page: (page.publication_date, page.title),
                reverse=True
            )
            pub_year = '2070'
            for page in relevant_pages:
                updated = f' (updated {page.last_updated})' if page.last_updated else ''
                pub_date = page.publication_date
                if pub_date[0:4] < pub_year:
                    pub_year = pub_date[0:4]
                    tag_page.append(f'\n## {pub_year}\n')
                pub_monthday = pub_date[5:]
                tag_page.append(
                    f'- {pub_monthday} — <a id="{page.permalink.strip("/")}" class="internal-link" href="{page.permalink}">{page.title}</a>{updated}\n'
                )
        self.pages.append(Page(page = tag_page, folder = 'pages'))

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
