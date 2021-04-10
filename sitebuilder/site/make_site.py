import os
import subprocess
from loguru import logger
from typing import Dict, List, Optional, Set, Tuple

from sitebuilder.site.page import Page
from sitebuilder.site.site import Site


def make_site():
    subprocess.run(['bundle', 'exec', 'jekyll', 'build'])
    page_paths = [path for path in os.listdir('pages/') if path != '.DS_Store']
    library_paths = [path for path in os.listdir('library/') if path != '.DS_Store']

    home_page = Page(page=read_page('index.md'), folder='')
    written_pages = [Page(page=read_page(f'pages/{page_path}'), folder='pages') for page_path in page_paths]
    library_pages = [Page(page=read_page(f'library/{library_path}'), folder='library') for library_path in library_paths]

    pages = [home_page] + written_pages + library_pages
    site = Site(pages=pages)
    site.update_backlinks()
    site.write_pages()
    subprocess.run(['bundle', 'exec', 'jekyll', 'build'])

def read_page(filepath: str):
    """Read in a page."""
    with open(filepath, 'rt') as f:
        return f.readlines()
