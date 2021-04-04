import click

from sitebuilder.sitebuilder.library.make_library import make_library

@click.command
def build_library_pages():
    library = make_library()
    library.make_shelf_pages()