from typing import List

from sitebuilder.library.author import Author
from sitebuilder.library.book import Book
from sitebuilder.library.reading import Reading
from sitebuilder.library.shelf import Shelf


class Library:

    def __init__(self, authors: List[Author], books: List[Book], readings: List[Reading]):
        self.authors = authors
        self.books = books
        self.readings = readings

    def get_shelves_by_publicaton_date(self):
        date_categories = {
            '<1000': (-9999, 999),
            '1000s': (1000, 1099),
            '1100s': (1100, 1199),
            '1200s': (1200, 1299),
            '1300s': (1300, 1399),
            '1400s': (1400, 1499),
            '1500s': (1500, 1599),
            '1600s': (1600, 1699),
            '1700s': (1700, 1799),
            '1800s': (1800, 1899),
            '1900s': (1900, 1909),
            '1910s': (1910, 1919),
            '1920s': (1920, 1929),
            '1930s': (1930, 1939),
            '1940s': (1940, 1949),
            '1950s': (1950, 1959),
            '1960s': (1960, 1969),
            '1970s': (1970, 1979),
            '1980s': (1980, 1989),
            '1990s': (1990, 1999),
            '2000': 2000,
            '2001': 2001,
            '2002': 2002,
            '2003': 2003,
            '2004': 2004,
            '2005': 2005,
            '2006': 2006,
            '2007': 2007,
            '2008': 2008,
            '2009': 2009,
            '2010': 2010,
            '2011': 2011,
            '2012': 2012,
            '2013': 2013,
            '2014': 2014,
            '2015': 2015,
            '2016': 2016,
            '2017': 2017,
            '2018': 2018,
            '2019': 2019,
            '2020': 2020,
            '2021': 2021
        }

    def get_shelves_by_read_date(self):
        date_categories = {
            '<2010': 'Before 2010',
            '2010': 2010,
            '2011': 2011,
            '2012': 2012,
            '2013': 2013,
            '2014': 2014,
            '2015': 2015,
            '2016': 2016,
            '2017': 2017,
            '2018': 2018,
            '2019': 2019,
            '2020': 2020,
            '2021': 2021
        }

    def get_shelves_by_genre(self):