import scrapy
import json
import time

start_time = time.time()

class muaBanBdsSpider(scrapy.Spider):
    name = 'muaban'
    headers = {
        "accept": "application/json",
        "accept-encoding": "gzip, deflate, br",
        "accept-language": "en-US,en;q=0.9",
        "cache-control": "no-cache",
        "content-type": "application/json",
        "origin": "https://nha.chotot.com",
        "pragma": "no-cache",
        "referer": "https://nha.chotot.com/",
        "sec-fetch-dest": "empty",
        "sec-fetch-mode": "cors",
        "sec-fetch-site": "same-site",
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.75 Safari/537.36"
    }

    base_url = 'https://gateway.chotot.com/v1/public/ad-listing'
    def start_requests(self):
        with open('city_name.json') as f:
            data = json.load(f)
            for temp in data:
                for region in temp.keys():
                    query_string_params = '?region_v2='+ region+ '&cg=1000&limit=50&o=50&st=s,k&page=1'
                    yield scrapy.Request(
                        url=self.base_url + query_string_params,
                        method='GET',
                        headers=self.headers,
                        callback=self.parse_page,
                        meta= {
                            "region": region
                        }
                    )
    def parse_page(self, response):
        data = json.loads(response.body)
        region = response.meta["region"]
        total_ads = 0
        if ('total' in data.keys()):
            if(int(data['total'])>0):
                total_ads = data['total']
            else:
                return
        number_page = round(total_ads/50)
        for page in range(1,number_page+1):
            query_string_params ='?region_v2='+ region+ '&cg=1000&limit=50&o=' + str((page-1)*50) + '&st=s,k&page=' + str(page)
            yield scrapy.Request(
                    url=self.base_url + query_string_params,
                    method='GET',
                    headers=self.headers,
                    callback=self.parse_ads
                )
    def parse_ads(self, response):
        data = json.loads(response.body)
        for ad in data['ads']:
            yield scrapy.Request(
                url=self.base_url+ "/" + str(ad['list_id']),
                method='GET',
                headers=self.headers,
                callback=self.parse_ad_detail,
                )

    def parse_ad_detail(self, response):
        data = json.loads(response.body)
        yield {
            "data": data
        }

        
