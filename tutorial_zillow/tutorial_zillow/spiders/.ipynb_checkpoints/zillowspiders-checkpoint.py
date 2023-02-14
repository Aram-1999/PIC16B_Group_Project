import scrapy 

class zillowspider(scrapy.Spider):
        name = "zillow"
        
        start_urls = ["https://www.zillow.com/phoenix-az/?searchQueryState=%7B%22pagination%22%3A%7B%7D%2C%22mapBounds%22%3A%7B%22west%22%3A-112.41459846496582%2C%22east%22%3A-111.82339668273926%2C%22south%22%3A33.23403062777737%2C%22north%22%3A33.7117126527925%7D%2C%22regionSelection%22%3A%5B%7B%22regionId%22%3A40326%2C%22regionType%22%3A6%7D%5D%2C%22isMapVisible%22%3Atrue%2C%22filterState%22%3A%7B%22sort%22%3A%7B%22value%22%3A%22days%22%7D%2C%22ah%22%3A%7B%22value%22%3Atrue%7D%7D%2C%22isListVisible%22%3Atrue%2C%22mapZoom%22%3A11%7D"]
        
        def parse(self,response):
            
            for block in response.css("div.StyledPropertyCardDataArea-c11n-8-82-3__sc-yipmu-0.eTKvfN"):
                for text in response.css("div.StyledPropertyCardDataArea-c11n-8-82-3__sc-yipmu-0.eTKvfN"):
                    print(response.css("li b::text").get())
