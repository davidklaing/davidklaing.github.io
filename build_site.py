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
        self.front_matter, self.content = self.separate_sections()
        self.title = self.get_attribute('title')
        self.permalink = self.get_attribute('permalink')
        self.backlinks = backlinks
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
    
    def get_attribute(self, attribute: str) -> str:
        """Get a page attribute, i.e. one of the lines in its front matter."""
        attribute_line, *_ = [line for line in self.front_matter if f'{attribute}: ' in line]
        return attribute_line.strip(f'{attribute}: ').strip('\n')
    
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
    
    def write_tooltips(self):
        """Write a new set of tooltips."""
        all_links = set(self.backlinks + self.forward_links) - {
            '<a id="home" class="internal-link" href="/">davidklaing.com</a>',
            '<a id="subscribe" class="internal-link" href="/subscribe/">Subscribe</a>'
        }
        non_tooltips_lines = [line for line in self.front_matter if 'tooltips: ' not in line and '- path:' not in line]
        tooltip_script_paths = [f'tooltip_{self.find_page_id(link)}.js' for link in all_links]
        if tooltip_script_paths:
            non_tooltips_lines.insert(-1, 'tooltips: \n- path: ' + '\n- path: '.join(tooltip_script_paths) + '\n')
        self.front_matter = non_tooltips_lines
    
    @staticmethod
    def find_page_id(link):
        soup = BeautifulSoup(link, 'html.parser')
        return soup.find('a').get('id')
    
    def write_backlinks(self) -> None:
        """Write a new set of backlinks, based on what was passed in with this instance of the page."""
        non_backlinks_lines = [line for line in self.front_matter if 'backlinks: ' not in line]
        if self.backlinks:
            non_backlinks_lines.insert(-1, 'backlinks: <ul><li>' + '</li><li>'.join(self.backlinks) + '</li></ul>\n')
        self.front_matter = non_backlinks_lines



class Database:
    """A representation a database of pages.

    @param pages: A list of Page instances.
    @param site_html_paths: A list of paths to the html pages in the _site folder.

    """

    def __init__(self, pages: List[Page], site_html_paths: List[str]):
        self.pages = pages
        self.site_html_paths = site_html_paths
        self.titles_dict: Dict[str, str] = {page.permalink: page.title for page in self.pages}

    def update_backlinks(self):
        """Update all the backlinks in the database."""
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
        return list(set(backlinks))
    
    def make_anchor_tag(self, permalink: str) -> str:
        """Make an anchor tag, given a page's permalink."""
        if permalink == '/':
            id = 'home'
        else:
            id = permalink.strip('/')
        title = self.titles_dict[permalink]
        return f'<a id="{id}" class="internal-link" href="{permalink}">{title}</a>'
    
    def update_tooltips(self):
        for page in self.pages:
            page.write_tooltips()
    
    def write_pages(self):
        """Write the pages back to markdown."""
        for page in self.pages:
            if page.permalink == '/':
                write_page(filepath=f'index.md', content=''.join(page.front_matter + page.content))
            else:
                path = page.permalink.strip('/') + '.md'
                write_page(filepath=f'pages/{path}', content=''.join(page.front_matter + page.content))
    
    def write_tooltips(self):
        for path in self.site_html_paths:
            page_id = self.get_id_from_path(path=path)
            tooltip = self.create_tooltip(path=path, page_id=page_id)
            write_page(filepath=f'_includes/tooltip_{page_id}.js', content=tooltip)
    
    def get_id_from_path(self, path):
        if path == '_site/index.html':
            return 'home'
        else:
            return path.replace('_site/', '')
    
    def create_tooltip(self, path, page_id):
        template = self.tooltip_template(page_id)
        suffix = '/index.html' if path != '_site/index.html' else ''
        html_page = read_page(path + suffix)
        soup = BeautifulSoup(''.join(html_page), 'html.parser')
        content_markup = soup.find("div", {"class": "article-content"}).contents
        content_string = ''.join([str(element) for element in content_markup]).replace('\n', '').replace("'", "\'")
        template.insert(-1, '    content: ' + "'" + content_string + "'\n")
        return ''.join(template)
    
    def tooltip_template(self, page_id):
        if page_id in ['home', 'subscribe']:
            placement = 'bottom'
        else:
            placement = 'right'
        return [
            "tippy('#" + page_id + "', {\n",
            "    theme: 'light-border',\n",
            "    arrow: false,\n",
            "    allowHTML: true,\n",
            f"    placement: '{placement}',\n",
            "    touch: false,\n",
            "    maxWidth: 550,\n",
            "    interactive: true,\n",
            "    interactiveBorder: 1,\n",
            "});"
        ]


def read_page(filepath):
    """Read in a page."""
    with open(filepath, 'rt') as f:
        return f.readlines()

def write_page(filepath, content):
    """Write a page."""
    with open(filepath, 'w') as f:
        return f.write(content)

def build_site():
    subprocess.run(['bundle', 'exec', 'jekyll', 'build'])
    page_paths = [path for path in os.listdir('pages/') if path != '.DS_Store']
    pages = [Page(page=read_page('index.md'))] \
        + [Page(page=read_page(f'pages/{page_path}')) for page_path in page_paths]
    site_html_paths = [
        '_site/' + path for path in os.listdir('_site/') 
        if path not in ['css', 'assets', 'README.md', 'build_site.py', 'build_library.py', 'library.csv']
    ]
    db = Database(pages=pages, site_html_paths=site_html_paths)
    db.update_backlinks()
    db.update_tooltips()
    db.write_pages()
    db.write_tooltips()
    subprocess.run(['bundle', 'exec', 'jekyll', 'build'])


if __name__ == "__main__":
    build_site()