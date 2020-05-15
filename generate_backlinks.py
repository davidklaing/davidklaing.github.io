import os
from bs4 import BeautifulSoup

def read_page(filepath):
    with open(filepath, 'rt') as f:
        return f.readlines()

def write_page(filepath, content):
    with open(filepath, 'w') as f:
        return f.write(content)

class Page:

    def __init__(self, page, backlinks = []):
        self.page = page
        self.front_matter, self.content = self.split()
        self.title = self.get_attribute('title')
        self.permalink = self.get_attribute('permalink')
        self.backlinks = backlinks
        self.write_backlinks()
        self.forward_links = self.get_forward_links()
        self.page = self.front_matter + self.content
    
    def split(self):
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
    
    def get_attribute(self, attribute):
        attribute_line, *_ = [line for line in self.front_matter if f'{attribute}: ' in line]
        return attribute_line.strip(f'{attribute}: ').strip('\n')
    
    def write_backlinks(self):
        non_backlinks_lines = [
            line for line in self.front_matter if 'backlinks: ' not in line
        ]
        non_backlinks_lines.insert(-1, 'backlinks: ' + ''.join(self.backlinks) + '\n')
        self.front_matter = non_backlinks_lines
    
    def get_forward_links(self):
        forward_links = []
        for line in self.content:
            forward_links += extract_links(line)
        return set(sorted(forward_links))

def extract_links(line):
    soup = BeautifulSoup(line)
    links = soup.find_all('a')
    if links:
        return [str(link) for link in links if link.get('href')[0] == '/']
    else:
        return []

class Database:

    def __init__(self, pages):
        self.pages = pages
        self.update_backlinks()
        self.write_pages()

    def update_backlinks(self):
        for page in self.pages:
            references = self.find_all_references(page)
            page.backlinks = references
            print(f'Backlinks for {page.title} are {references}')
            page.write_backlinks()

    def find_all_references(self, this_page):
        references = []
        for other_page in self.pages:
            if this_page.permalink != other_page.permalink:
                for link in other_page.forward_links:
                    soup = BeautifulSoup(link)
                    if soup.find('a').get('href') == this_page.permalink:
                        references.append(
                            self.make_anchor_tag(
                                title=self.find_title(other_page.permalink),
                                href=other_page.permalink
                            )
                        )
        return references
    
    def find_title(self, permalink):
        this_page, *_ = [page for page in self.pages if page.permalink == permalink]
        return this_page.title
    
    def make_anchor_tag(self, title, href):
        return f'<a id="{href}" href="{href}">{title}</a>'
    
    def write_pages(self):
        for page in self.pages:
            path = page.permalink.strip('/') + '.md'
            write_page(filepath=f'pages/{path}', content=''.join(page.front_matter + page.content))


page_paths = os.listdir('pages/')

pages = [Page(page = read_page(f'pages/{page_path}')) for page_path in page_paths]

db = Database(pages=pages)

for page in db.pages:
    print(page.title)
    print(page.front_matter)