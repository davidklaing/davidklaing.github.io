import pandas as pd

library = pd.read_csv('~/Documents/resources/goodreads_bookshelf/goodreads_library_export.csv')

read_list = library[library['Exclusive Shelf'] == 'read']

for col in read_list:
    print(col)

def get_lastname(author):
    author_list = author.split()
    return author_list[-1]

read_list['author_lastname'] = [get_lastname(author) for author in read_list['Author']]

for index, row in read_list.sort_values(by='author_lastname').iterrows():
    if row['My Rating'] >= 4:
        print(f"* {row['author_lastname']}, *{row['Title']}*, ({str(row['Original Publication Year'])[:-2]})")