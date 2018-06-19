import scrapy
import json


class RestaurantSpider(scrapy.Spider):
    name = "restaurants"
    start_urls = [
        'https://www.yamu.lk/place/restaurants?page=1',
    ]

    def parse(self, response):
        for restaurant in response.css('a.front-group-item'):
            url = restaurant.css('a::attr(href)').extract_first()+'#full'
            yield scrapy.Request(url=url, callback=self.parse_item)

        next_page = response.css('a[rel="next"]::attr(href)').extract_first()

        if next_page is not None:
            yield response.follow(next_page, self.parse)

    def parse_item(self, response):
        name = response.css('h2::text').extract_first()
        address = response.css('p.addressLine::text').extract_first().strip()
        telephone = response.css('a.emph::attr(href)').extract_first().split(":")[-1]
        open_until = response.css('p.open::text').extract_first()
        description = response.css('p.excerpt::text').extract_first()
        yamu_rating = response.css('div.place-rating-box-item')[0].css('p::text').extract_first()
        image_urls = []
        review = "";

        body = response.css('div.bodycopy')[0]

        for img in body.xpath('//img'):
            try:
                img_url = img.xpath('./@src').extract()[0]
                if (img_url[0] != 'h'):
                    img_url= 'https:'+ img_url

                image_urls.append(img_url)
                
            except Exception as e:
                print("no images")


        for paragraph in body.css('p::text').extract():
            review = review + paragraph.strip() + '\n'

        resaurant_posting = {
            'name' : name,
            'address' : address,
            'open_until' : open_until,
            'telephone' : telephone,
            'description' : description,
            'reviews' : review,
            'yamu_rating' : yamu_rating,
            'url' : response.url,
            'img_urls' : image_urls
        }

        file_name = 'restaurants/' + name + '.json'
        with open(file_name, 'w') as file:
            file.write(json.dumps(resaurant_posting, indent=2))
