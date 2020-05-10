import os
import re

pages = os.listdir('pages/')


def read_page(filepath):
    with open(filepath, 'rt') as f:
        return f.readlines()

class Page:

    def __init__(self, page, md_backlinks = []):
        self.page = page
        self.front_matter, self.content = self.split()
        self.title = self.get_title()
        self.md_backlinks = md_backlinks
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
    
    def get_title(self):
        title_line, *_ = [line for line in self.front_matter if 'title: ' in line]
        return title_line.strip('title: ').strip('\n')
    
    def write_backlinks(self):
        if self.md_backlinks:
            non_backlinks_lines = [
                line for line in self.front_matter if 'backlinks: ' not in line
            ]
            backlinks = []
            for link in self.md_backlinks:
                title, path = link.strip('[').strip(')').split('](')
                backlinks.append(create_backlink(title, path))
            non_backlinks_lines.insert(-1, 'backlinks: ' + ''.join(backlinks))
            self.front_matter = non_backlinks_lines
    
    def get_forward_links(self):
        forward_links = []
        for line in self.content:
            forward_links += extract_links(line)
        return set(sorted(forward_links))

def create_backlink(title, path):
    return f'<a href="{path}">{title}</a>'

def extract_links(line):
    return re.findall('\[[\w]*]\(/[\w]*\)', line)


example1_page = Page(
    page = read_page('pages/example1.md'), 
    md_backlinks = ['[Example 2](/example2)', '[About](/about)']
)

example1_page.front_matter