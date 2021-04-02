import scrapy

from scrapy.loader import ItemLoader

from ..items import BanknewportItem
from itemloaders.processors import TakeFirst


class BanknewportSpider(scrapy.Spider):
	name = 'banknewport'
	start_urls = ['https://www.banknewport.com/news/']

	def parse(self, response):
		post_links = response.xpath('//a[@class="title"]/@href').getall()
		yield from response.follow_all(post_links, self.parse_post)

	def parse_post(self, response):
		title = response.xpath('//div[@class="content"]/h1/text()').get()
		description = response.xpath('//div[@class="content_holder"]//text()[normalize-space()]').getall()
		description = [p.strip() for p in description if '{' not in p]
		description = ' '.join(description).strip()
		date = response.xpath('//div[@class="content"]/p/text()').get()

		item = ItemLoader(item=BanknewportItem(), response=response)
		item.default_output_processor = TakeFirst()
		item.add_value('title', title)
		item.add_value('description', description)
		item.add_value('date', date)

		return item.load_item()
