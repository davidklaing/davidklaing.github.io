import os
import subprocess

from bs4 import BeautifulSoup
from loguru import logger
from typing import Dict, List, Optional, Set, Tuple


class Page:
    """A representation of a page.
    
    @param page: A list of strings representing the markdown page.
    @param backlinks: A list of anchor tags representing the backlinks for this page.

    """

    def __init__(self, page: List[str], backlinks: List[str] = []):
        self.page = page
        self.front_matter, self.content = self.separate_front_matter_from_content()
        self.title = self.get_attribute('title')
        self.permalink = self.get_attribute('permalink')
        self.backlinks = backlinks
        self.write_backlinks()
        self.forward_links = self.get_forward_links()
        self.page = self.front_matter + self.content
    
    def separate_front_matter_from_content(self) -> Tuple[List[str], List[str]]:
        """Separate the page's front matter from its content."""
        front_matter = []
        content = []
        yaml_line_count = 0
        for line in self.page:
            if yaml_line_count < 2:
                front_matter.append(line)
            else:
                content.append(line)
            if line == '---\n':
                yaml_line_count += 1
        return front_matter, content
    
    def get_attribute(self, attribute: str) -> str:
        """Get a page attribute, i.e. one of the lines in its front matter."""
        attribute_line, *_ = [line for line in self.front_matter if f'{attribute}: ' in line]
        return attribute_line.strip(f'{attribute}: ').strip('\n')
    
    def write_backlinks(self) -> None:
        """Write a new set of backlinks, based on what was passed in with this instance of the page."""
        non_backlinks_lines = [line for line in self.front_matter if 'backlinks: ' not in line]
        non_backlinks_lines.insert(-1, 'backlinks: ' + ''.join(self.backlinks) + '\n')
        self.front_matter = non_backlinks_lines
    
    def get_forward_links(self) -> Set[str]:
        """Get all the links found in the content of this page."""
        forward_links = []
        for line in self.content:
            forward_links += self.extract_links(line)
        return set(sorted(forward_links))

    @staticmethod
    def extract_links(line: str) -> List[Optional[str]]:
        """Extract all links from a line in the content of the page."""
        soup = BeautifulSoup(line, 'html.parser')
        links = soup.find_all('a')
        return [str(link) for link in links if link.get('href')[0] == '/'] if links else []


class Database:
    """A representation a database of pages.

    @param pages: A list of Page instances.

    """

    def __init__(self, pages: List[Page]):
        self.pages = pages
        self.titles_dict: Dict[str, str] = {page.permalink: page.title for page in self.pages}

    def update_backlinks(self):
        """Update all the backlinks in the database."""
        for page in self.pages:
            page.backlinks = self.find_backlinks(this_page=page)
            page.write_backlinks()

    def find_backlinks(self, this_page: Page) -> Set[str]:
        """Find all backlinks for a given page."""
        references = []
        for other_page in self.pages:
            if this_page.permalink != other_page.permalink:
                for link in other_page.forward_links:
                    soup = BeautifulSoup(link, 'html.parser')
                    if soup.find('a').get('href') == this_page.permalink:
                        references.append(self.make_anchor_tag(permalink=other_page.permalink))
        return set(references)
    
    def make_anchor_tag(self, permalink: str) -> str:
        """Make an anchor tag, given a page's permalink."""
        id = permalink.strip("/")
        title = self.titles_dict[permalink]
        return f'<a id="{id}" class="internal-link" href="{permalink}">{title}</a>'
    
    def write_pages(self):
        """Write the pages back to markdown."""
        for page in self.pages:
            path = page.permalink.strip('/') + '.md'
            write_page(filepath=f'pages/{path}', content=''.join(page.front_matter + page.content))


def read_page(filepath):
    """Read in a page."""
    with open(filepath, 'rt') as f:
        return f.readlines()

def write_page(filepath, content):
    """Write a page."""
    with open(filepath, 'w') as f:
        return f.write(content)

if __name__ == "__main__":
    page_paths = os.listdir('pages/')
    pages = [Page(page = read_page(f'pages/{page_path}')) for page_path in page_paths]
    db = Database(pages=pages)
    db.update_backlinks()
    db.write_pages()
    subprocess.run(['bundle', 'exec', 'jekyll', 'build'])