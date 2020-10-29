import scrapy
import json

class choThueBdsSpider(scrapy.Spider):
    name = 'chothuebds'
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
        "user-agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 12_4_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/12.1.2 Mobile/15E148 Safari/604.1"
    }

    base_url = 'https://gateway.chotot.com/v1/public/ad-listing'

    def start_requests(self):
        category = '1000'

        with open('region.json') as f:
            data = json.load(f.read())
            area = ''
            for i in range(0,len(data)):
                for a in data[i].keys():
                    if a == 'id_region':
                        continue
                    area = str(a)
                region = data[i]['id_region']
                for w in data[i][area]:
                    ward = str(w['id'])
                    query_string_params = '?region_v2=' + region + '&area_v2='+ area +'&ward=' + ward + '&cg='+ category +'&limit=50'
                    yield scrapy.Request(
                        url=self.base_url + query_string_params,
                        method='GET',
                        headers=self.headers,
                        callback=self.parse_page,
                        meta= {
                            "region": region,
                            "area": area,
                            "ward": ward,
                            "category": category
                        }
                    )

    def parse_page(self, response):
        data = json.loads(response.body)
        self.log(data)
        region = response.meta["region"]
        area= response.meta["area"]
        ward = response.meta["ward"]
        category = response.meta["category"]
        total_ads = 0
        if ('total' in data.keys()):
            if(int(data['total'])>0):
                total_ads = data['total']
            else:
                return

        number_page = round(total_ads/50)
        for page in range(1,number_page+1):
            query_string_params = '?region_v2=' + region + '&area_v2='+ area +'&ward=' + ward + '&cg='+ category +'&limit=50&o='+ str((page-1)*50) +'&st=u,h&page=' + str(page)
            yield scrapy.Request(
                url=self.base_url + query_string_params,
                method='GET',
                headers=self.headers,
                callback=self.parse_ads,
                meta= {
                    "region": region,
                    "area": area,
                    "ward": ward,
                    "category": category
                }
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

        
