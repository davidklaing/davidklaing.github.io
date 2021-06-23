import os
import subprocess
from loguru import logger
from typing import Dict, List, Optional, Set, Tuple

from sitebuilder.site.page import Page
from sitebuilder.site.site import Site


def make_site():
    subprocess.run(['bundle', 'exec', 'jekyll', 'build'])

    page_categories = [
        'automatically-created', 
        'essays', 
        'library', 
        'notes', 
        'retrospectives', 
        'reviews'
    ]

    home_page = Page(page=read_page('index.md'), folder='')
    pages = [home_page]

    for category in page_categories:
        category_paths = [path for path in os.listdir(f'pages/{category}/') if path != '.DS_Store']
        category_pages = [
            Page(page=read_page(f'pages/{category}/{path}'), folder=f'pages/{category}') 
            for path in category_paths
        ]
        pages += category_pages

    site = Site(pages=pages)
    site.update_backlinks()
    site.write_pages()
    subprocess.run(['bundle', 'exec', 'jekyll', 'build'])

def read_page(filepath: str):
    """Read in a page."""
    with open(filepath, 'rt') as f:
        return f.readlines()
