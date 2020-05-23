import pandas as pd

library = pd.read_csv('~/Documents/resources/goodreads_bookshelf/goodreads_library_export.csv')

read_list = library[library['Exclusive Shelf'] == 'read']

for col in library:
    print(col)

for index, row in read_list.iterrows():
    print(row['Author'], row['Title'], row['My Rating'])