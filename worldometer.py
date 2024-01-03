import scrapy


class WorldometerSpider(scrapy.Spider):
    name = "worldometer"
    allowed_domains = ["www.worldometers.info"]
    start_urls = ["https://www.worldometers.info/world-population/population-by-country"]

    def parse(self, response):
        title=response.xpath("//h1/text()").get()
        countries=response.xpath("//td/a")
        for country in countries:
            name=country.xpath(".//text()").get()
            link=country.xpath(".//@href").get()
            #absolute_url=f"https://www.worldometers.info{link}"
            #yield scrapy.Request(absolute_url)

            #absolute_url=response.urljoin(link)
            #yield scrapy.Request(absolute_url)

            yield response.follow(link,callback=self.parse_country,meta={"country":name})

            #yield  {
            #  "titles":name,
            #    "countries_link":link,
            #}

    def parse_country(self,response):
        data=response.xpath('(//table[@class="table table-striped table-bordered table-hover table-condensed table-list"])[1]/tbody/tr')
        country=response.request.meta["country"]
        for i in data:
            year=i.xpath(".//td[1]/text()").get()
            population=i.xpath(".//td[2]/strong/text()").get()
            yield{
                "country":country,
                "year":year,
                "population":population,
            }
