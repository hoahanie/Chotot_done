import scrapy
import json


class QuettentpSpider(scrapy.Spider):
    name = 'quetthongtin'
    headers = {
            "accept": "*/*",
            "accept-encoding": "gzip, deflate, br",
            "accept-language": "en-US,en;q=0.9",
            "cache-control": "no-cache",
            "origin": "https://nha.chotot.com",
            "pragma": "no-cache",
            "referer": "https://nha.chotot.com/",
            "sec-fetch-dest": "empty",
            "sec-fetch-mode": "cors",
            "sec-fetch-site": "same-site",
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.75 Safari/537.36"
        }

    def start_requests(self):
        url = 'https://gateway.chotot.com/v1/public/web-proxy-api/loadRegions' 
        yield scrapy.FormRequest(
            url=url,
            method='GET',
            headers=self.headers,
            callback=self.parse_district
        )
    def parse_district(self, response):
        data = json.loads(response.body)
        regions = data["regionFollowId"]["entities"]["regions"]
        for region in regions:
            yield {
                region: regions[region]["name"]
            }