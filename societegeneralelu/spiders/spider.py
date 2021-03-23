import scrapy

from scrapy.loader import ItemLoader

from ..items import SocietegeneraleluItem
from itemloaders.processors import TakeFirst

import requests

url = "https://www.societegenerale.lu/fr/societe-generale-luxembourg/communiques-presse-actualites/"

base_payload = "tx_bisgsummary_pi2%5Bpage%5D={}&tx_bisgsummary_pi2%5Btext%5D=&tx_bisgsummary_pi2%5Byear%5D=0&tx_bisgsummary_pi2%5BremoveWrapperToListing%5D=true&no_cache=true&tx_bisgsummary_pi2%5BajaxCall%5D=true&tx_bisgsummary_pi2%5BajaxMethod%5D=refreshResults&tx_bisgsummary_pi2%5BforceConf%5D=&tx_bisgsummary_pi2%5BidContent%5D=13134"
headers = {
  'authority': 'www.societegenerale.lu',
  'pragma': 'no-cache',
  'cache-control': 'no-cache',
  'sec-ch-ua': '"Google Chrome";v="89", "Chromium";v="89", ";Not A Brand";v="99"',
  'accept': 'text/html, */*; q=0.01',
  'x-requested-with': 'XMLHttpRequest',
  'sec-ch-ua-mobile': '?0',
  'user-agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.90 Safari/537.36',
  'content-type': 'application/x-www-form-urlencoded; charset=UTF-8',
  'origin': 'https://www.societegenerale.lu',
  'sec-fetch-site': 'same-origin',
  'sec-fetch-mode': 'cors',
  'sec-fetch-dest': 'empty',
  'referer': 'https://www.societegenerale.lu/fr/societe-generale-luxembourg/communiques-presse-actualites/',
  'accept-language': 'en-US,en;q=0.9,bg;q=0.8',
  'cookie': 'civicAllowCookies=yes; _ga=GA1.2.781032923.1616422955; _gid=GA1.2.1248201824.1616422955; _pk_ses.186.cb62=1; _pk_id.186.cb62=be2f692b2d249855.1616422955.1.1616422993.1616422955.; SERVERID=f0'
}


class SocietegeneraleluSpider(scrapy.Spider):
	name = 'societegeneralelu'
	start_urls = ['https://www.societegenerale.lu/fr/societe-generale-luxembourg/communiques-presse-actualites/']
	page = 1

	def parse(self, response):
		payload = base_payload.format(self.page)
		data = requests.request("POST", url, headers=headers, data=payload)
		raw_data = scrapy.Selector(text=data.text)
		post_links = raw_data.xpath('//div[contains(@id, "card2")]/@data-ref').getall()
		for post in post_links:
			link = 'https://www.societegenerale.lu/fr/type/1234/ajaxsid/' + post
			yield response.follow(link, self.parse_post)

		if post_links:
			self.page += 1
			yield response.follow(response.url, self.parse, dont_filter=True)

	def parse_post(self, response):
		title = response.xpath('//h1/text()').get()
		description = response.xpath('//div[@class="intro" or @class="sgnews_single_content"]//text()[normalize-space()]').getall()
		description = [p.strip() for p in description]
		description = ' '.join(description).strip()
		date = response.xpath('//div[@class="sgnews_single_date"]/text()').get()

		item = ItemLoader(item=SocietegeneraleluItem(), response=response)
		item.default_output_processor = TakeFirst()
		item.add_value('title', title)
		item.add_value('description', description)
		item.add_value('date', date)

		return item.load_item()
