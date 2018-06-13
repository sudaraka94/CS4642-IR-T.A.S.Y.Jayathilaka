import scrapy


class RestaurantSpider(scrapy.Spider):
    name = "restaurants"
    start_urls = [
        'https://www.yamu.lk/place/restaurants?page=1',
    ]

    def parse(self, response):
        for restaurant in response.css('a.front-group-item'):
            yield {
                'name': restaurant.xpath('div/h3/text()').extract_first(),
            }

        next_page = response.css('a[rel="next"]::attr(href)').extract_first()

        if next_page is not None:
            yield response.follow(next_page, self.parse)
