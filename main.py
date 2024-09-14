import scrapy

class QuotesSpider(scrapy.Spider):
    name = "quotes"
    start_urls = ['http://quotes.toscrape.com']

    def parse(self, response):
        # Збір цитат
        for quote in response.css('div.quote'):
            yield {
                'text': quote.css('span.text::text').get(),
                'author': quote.css('span small.author::text').get(),
                'tags': quote.css('div.tags a.tag::text').getall(),
            }

        # Збір авторів
        for author in response.css('small.author'):
            author_url = response.css(f'a[href*="{author.get()}"]::attr(href)').get()
            yield response.follow(author_url, self.parse_author)

        # Перехід на наступні сторінки
        next_page = response.css('li.next a::attr(href)').get()
        if next_page is not None:
            yield response.follow(next_page, self.parse)

    def parse_author(self, response):
        yield {
            'name': response.css('h3.author-title::text').get().strip(),
            'birthdate': response.css('span.author-born-date::text').get(),
            'bio': response.css('div.author-description::text').get().strip(),
        }
