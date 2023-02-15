import scrapy 
from scrapy.http import Request

class zillowspider(scrapy.Spider):
        name = "zillow"
        
        start_urls = ["https://www.zillow.com/phoenix-az/houses/?searchQueryState=%7B%22pagination%22%3A%7B%7D%2C%22usersSearchTerm%22%3A%22Phoenix%2C%20AZ%22%2C%22mapBounds%22%3A%7B%22west%22%3A-112.54665134179687%2C%22east%22%3A-111.59908054101562%2C%22south%22%3A33.156472387949066%2C%22north%22%3A34.11004882322404%7D%2C%22regionSelection%22%3A%5B%7B%22regionId%22%3A40326%2C%22regionType%22%3A6%7D%5D%2C%22isMapVisible%22%3Atrue%2C%22filterState%22%3A%7B%22con%22%3A%7B%22value%22%3Afalse%7D%2C%22apa%22%3A%7B%22value%22%3Afalse%7D%2C%22mf%22%3A%7B%22value%22%3Afalse%7D%2C%22ah%22%3A%7B%22value%22%3Atrue%7D%2C%22sort%22%3A%7B%22value%22%3A%22globalrelevanceex%22%7D%2C%22land%22%3A%7B%22value%22%3Afalse%7D%2C%22tow%22%3A%7B%22value%22%3Afalse%7D%2C%22manu%22%3A%7B%22value%22%3Afalse%7D%2C%22apco%22%3A%7B%22value%22%3Afalse%7D%7D%2C%22isListVisible%22%3Atrue%7D"]
        
        def parse(self,response):    
            for house in response.css("article a::attr(href)").getall():
                yield scrapy.Request(house,callback = self.parse_at_home)
            url = response.css("#grid-search-results > div.search-pagination > nav > ul:last-child a::attr(href)").getall()
            next_page = "https://www.zillow.com" + url[-1]    
            yield scrapy.Request(next_page, callback=self.parse)
            
        def parse_at_home(self,response):
            pass
            price = response.css('div.hdp__sc-1s2b8ok-1.hGMTgV span:first-of-type span::text').get()
            info = response.css('span.Text-c11n-8-73-0__sc-aiai24-0.kHeRng strong::text').getall()
            address = response.css('h1.Text-c11n-8-73-0__sc-aiai24-0.kHeRng::text').getall()

            yield {
                 "price": int(price[1:].replace(',', '')),
                 "bed": int(info[0]),
                 "bath": int(info[1]),
                 "sqft": int(info[2].replace(',', '')),
                 "address": address
            }
            
