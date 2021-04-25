from typing import Dict, List, Optional, Set, Tuple

from bs4 import BeautifulSoup


class Page:
    """A representation of a page.
    
    @param page: A list of strings representing the markdown page.
    @param backlinks: A list of anchor tags representing the backlinks for this page.

    """

    def __init__(self, page: List[str], folder = str, backlinks: List[str] = []):
        self.page = page
        self.folder = folder
        self.front_matter, self.content = self.separate_sections()
        self.title = self.get_attribute('title')
        self.permalink = self.get_attribute('permalink')
        self.publication_date = self.get_attribute('publication_date')
        self.last_updated = self.get_attribute('last_updated')
        self.backlinks = sorted(backlinks)
        self.forward_links = self.get_forward_links()
    
    def separate_sections(self) -> Tuple[List[str], List[str]]:
        """Separate the page's front matter from its content."""
        front_matter = []
        content = []
        yaml_line_count = 0
        for line in self.page:
            if yaml_line_count < 2:
                front_matter.append(line)
            elif yaml_line_count >= 2:
                content.append(line)
            if line == '---\n':
                yaml_line_count += 1
        return front_matter, content
    
    def get_attribute(self, attribute: str) -> Optional[str]:
        """Get a page attribute, i.e. one of the lines in its front matter."""
        attribute_lines = [line for line in self.front_matter if f'{attribute}: ' in line]
        if attribute_lines:
            return attribute_lines[0].strip(f'{attribute}: ').strip('\n')
        else:
            return None
    
    def get_forward_links(self) -> Set[str]:
        """Get all the links found in the content of this page."""
        forward_links = []
        for line in self.content:
            forward_links += self.extract_links(line)
        return list(set(sorted(forward_links)))

    @staticmethod
    def extract_links(line: str) -> List[Optional[str]]:
        """Extract all links from a line in the content of the page."""
        soup = BeautifulSoup(line, 'html.parser')
        links = soup.find_all('a')
        return [str(link) for link in links if link.get('href')[0] == '/'] if links else []
    
    @staticmethod
    def find_page_id(link):
        soup = BeautifulSoup(link, 'html.parser')
        return soup.find('a').get('id')
    
    def write_backlinks(self) -> None:
        """Write a new set of backlinks, based on what was passed in with this instance of the page."""
        non_backlinks_lines = [line for line in self.front_matter if 'backlinks: ' not in line]
        if self.backlinks:
            non_backlinks_lines.insert(-1, 'backlinks: \'<ul><li>' + '</li><li>'.join(self.backlinks) + '</li></ul>\'\n')
        self.front_matter = non_backlinks_lines