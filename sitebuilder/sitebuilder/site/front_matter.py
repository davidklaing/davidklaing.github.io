class FrontMatter:

    def __init__(
        self, 
        title, 
        permalink, 
        published, 
        publication_date = None, 
        last_updated = None, 
        tags = None,
        backlinks = None
    ):
        self.title = title
        self.permalink = permalink
        self.published = published
        self.publication_date = publication_date
        self.last_updated = last_updated
        self.tags = tags
        self.backlinks = backlinks
    
    def create_front_matter(self):
        front_matter = [
            '---\n',
            'layout: page\n',
            f'title: {self.title}\n',
            f'permalink: {self.permalink}\n',
            f'published: {self.published}\n'
        ]
        if self.publication_date:
            front_matter.append(f'publication_date: {self.publication_date}\n')
        if self.last_updated:
            front_matter.append(f'last_updated: {self.last_updated}\n')
        if self.tags:
            front_matter.append(f'tags: {self.tags}\n')
        if self.backlinks:
            front_matter.append(f'backlinks: {self.backlinks}\n')
        else:
            front_matter.append(f'backlinks: \n')
        front_matter += [
            '---\n',
            '\n'
        ]
        return front_matter