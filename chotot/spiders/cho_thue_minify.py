import scrapy
import json


class cho_thue_minifySpider(scrapy.Spider):
    name = 'chothue_minify'
    headers_city = {
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
        "user-agent": "Mozilla/5.0 (Windows NT 5.1; rv:36.0) Gecko/20100101 Firefox/36.0"
    }
    headers_chothue = {
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
    base_url = 'https://gateway.chotot.com/v1/public/ad-listing?region_v2='

    def start_requests(self):
        url ='https://gateway.chotot.com/v1/public/web-proxy-api/loadRegions'
        yield scrapy.FormRequest(
            url=url,
            method='GET',
            headers=self.headers_city,
            callback=self.parse_district
        )
    def parse_district(self, response):
        data = json.loads(response.body)
        regions = data["regionFollowId"]["entities"]["regions"]
        for region in regions:
            query_string_params = region+ '&cg=1000&limit=50&o=0&st=u,h&page=1'
            yield scrapy.Request(
                url=self.base_url + query_string_params,
                method='GET',
                headers=self.headers_chothue,
                callback=self.parse_chothue,
                meta= {
                    "region": region
                }
            )
    def parse_chothue(self,response):
        data = json.loads(response.body)
        region = response.meta["region"]
        total_projects = 0
        if ('total' in data.keys()):
            if(int(data['total'])>0):
                total_projects = data['total']
            else:
                return
        number_page = round(total_projects/50)

        for page in range(1,number_page+1):
            query_string = region + '&cg=1000&limit=50&o=' + str((page-1)*50) + '&st=u,h&page='+ str(page)
            yield scrapy.Request(
                url=self.base_url + query_string,
                method='GET',
                headers=self.headers_chothue,
                callback=self.parse_page,
            )

    def parse_page(self,response):
        data = json.loads(response.body)
        yield {
            "data": data
        }

