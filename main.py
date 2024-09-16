# main.py
import scrapy
import json
import os
from pymongo import MongoClient
from dotenv import load_dotenv

class QuotesSpider(scrapy.Spider):
    name = "quotes"
    start_urls = ['http://quotes.toscrape.com']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        load_dotenv()
        self.mongodb_uri = os.getenv('MONGODB_URI')
        self.client = MongoClient(self.mongodb_uri)
        self.db = self.client.get_database()

    def parse(self, response):
        
        for quote in response.css('div.quote'):
            quote_data = {
                'text': quote.css('span.text::text').get(),
                'author': quote.css('span small.author::text').get(),
                'tags': quote.css('div.tags a.tag::text').getall(),
            }
            
            self.db.quotes.insert_one(quote_data)
            yield quote_data

            
            author_url = quote.css('small.author ~ a::attr(href)').get()
            if author_url is not None:
                yield response.follow(author_url, self.parse_author)

        
        next_page = response.css('li.next a::attr(href)').get()
        if next_page is not None:
            yield response.follow(next_page, self.parse)

    def parse_author(self, response):
        author_data = {
            'name': response.css('h3.author-title::text').get().strip(),
            'birthdate': response.css('span.author-born-date::text').get(),
            'bio': response.css('div.author-description::text').get().strip(),
        }
        
        self.db.authors.insert_one(author_data)
        yield author_data

    def close(self, reason):
        self.client.close()
