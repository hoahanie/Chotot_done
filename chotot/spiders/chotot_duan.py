import scrapy
import json

class choThueBdsSpider(scrapy.Spider):
    name = 'duanbds'
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
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/52.0.2743.116 Safari/537.36 Edge/15.15063"
    }
    base_url = 'https://gateway.chotot.com/v1/public/xproperty/projects/_search'
    def start_requests(self):
        with open('region.json') as f:
            data = json.load(f.read())
            for i in range(0,len(data)):
                region = data[i]['id_region']
                query_string_params = '?region_v2=' + region+ '&offset=0&status=active'
                yield scrapy.Request(
                    url=self.base_url + query_string_params,
                    method='GET',
                    headers=self.headers,
                    callback=self.parse_page,
                    meta= {
                        "region": region
                    }
                )
    def parse_page(self,response):
        data = json.loads(response.body)
        self.log(data)
        region = response.meta["region"]
        total_projects = 0
        if ('total' in data.keys()):
            if(int(data['total'])>0):
                total_projects = data['total']
            else:
                return
        
        number_page = round(total_projects/10)
        self.log(number_page)
        for page in range(1,number_page+1):
            query_string_params = '?region_v2=' + region + '&offset=' + str((page-1)*10) + '&status=active'
            self.log(self.base_url + query_string_params)
            yield scrapy.Request(
                url=self.base_url + query_string_params,
                method='GET',
                headers=self.headers,
                callback=self.parse_project,
                meta= {
                    "region": region
                }
            )
    def parse_project(self,response):
        data = json.loads(response.body)
        yield {
            "data": data
        }
        