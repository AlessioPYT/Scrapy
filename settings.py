FEEDS = {
    'quotes.json': {
        'format': 'json',
        'encoding': 'utf8',
        'store_empty': False,
        'fields': ['text', 'author', 'tags'],
        'indent': 4,
    },
    'authors.json': {
        'format': 'json',
        'encoding': 'utf8',
        'store_empty': False,
        'fields': ['name', 'birthdate', 'bio'],
        'indent': 4,
    },
}
