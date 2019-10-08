"""
create by jxh @2019/6/28
"""
import json
import time
import requests
import re
import multiprocessing

from handle_insert_data import la_gou_mysql


class HandelLaGou:
    def __init__(self):
        self.lagou_session = requests.session()
        self.header = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, '
                          'like Gecko) Chrome/72.0.3626.109 Safari/537.36'
        }
        self.city_list = ""

    def handle_city_job(self, city):
        # first_request_url = "https://www.lagou.com/jobs/list_python?px=default&gx=%E5%85%A8%E8%81%8C&city=%{}".format(city)
        first_request_url = "https://www.lagou.com/jobs/list_python?city=%s&cl=false&fromSearch=true&labelWords=&suginput=" % city
        print(first_request_url)
        first_response = self.handle_request(url=first_request_url, method='GET')
        total_page_search = re.compile(r'class="span\stotalNum">(\d+)</span>')
        try:
            total_page = total_page_search.search(first_response).group(1)
        except:
            return
        else:
            for i in range(1, int(total_page) + 1):
                data = {
                    "pn": i,
                    "kd": "python"
                }
                page_url = "https://www.lagou.com/jobs/positionAjax.json?city=%s&needAddtionalResult=false" % city
                referer_url = "https://www.lagou.com/jobs/list_python?city=%s&cl=false&fromSearch=true&" \
                              "labelWords=&suginput=" % city
                self.header['Referer'] = referer_url.encode()
                response = self.handle_request(url=page_url, method='POST', data=data, info=city)
                la_gou_data = json.loads(response)
                job_lists = la_gou_data['content']['positionResult']['result']
                for job in job_lists:
                    # print(job)
                    la_gou_mysql.inset_item(job)
                # print(response)

        print(total_page)

    def handel_city(self):
        # city_search = re.compile(r'zhaopin/">(.*?)</a>')
        city_search = re.compile(r'www\.lagou\.com\/.*\/">(.*?)</a>')
        city_url = "https://www.lagou.com/jobs/allCity.html"
        city_result = self.handle_request(url=city_url, method='GET')
        self.city_list = city_search.findall(city_result)
        # print(city_result)
        # print(self.city_list)
        self.lagou_session.cookies.clear()

    def handle_request(self, url, method, data=None, info=None):
        while True:
            if method == 'GET':
                response = self.lagou_session.get(url=url, headers=self.header)
            elif method == 'POST':
                response = self.lagou_session.post(url=url, headers=self.header, data=data)
            response.encoding = 'utf-8'
            if '太频繁' in response.text:
                print(response.text)
                self.lagou_session.cookies.clear()
                first_request_url = "https://www.lagou.com/jobs/list_python?city=%s&cl=false&" \
                                    "fromSearch=true&labelWords=&suginput=" % info
                self.handle_request(url=first_request_url, method='GET')
                time.sleep(10)
                continue
            return response.text

    # def handle_request(self, url, method, data=None, info=None):
    #     # 加入阿布云的动态代理
    #     # proxy_info = "http://%s:%s@%s:%s" % ('H1V32R6470A7G90D', 'CD217C660A9143C3', 'http-dyn.abuyun.com', '9020')
    #     # proxy = {
    #     #     "http": proxy_info,
    #     #     "https": proxy_info
    #     # }
    #     while True:
    #         # try:
    #         if method == 'GET':
    #             # response = self.lagou_session.get(url=url, headers=self.header, proxies=proxy, timeout=6)
    #             response = self.lagou_session.get(url=url, headers=self.header)
    #         elif method == 'POST':
    #             # response = self.lagou_session.post(url=url, headers=self.header, data=data, proxies=proxy, timeout=6)
    #             response = self.lagou_session.post(url=url, headers=self.header, data=data)
    #         # except:
    #         #     self.lagou_session.cookies.clear()
    #         #     first_request_url = "https://www.lagou.com/jobs/list_python?city=%s&cl=false&" \
    #         #                         "fromSearch=true&labelWords=&suginput=" % info
    #         #     self.handle_request(url=first_request_url, method='GET')
    #         #     time.sleep(10)
    #         #     continue
    #     response.encoding = 'utf-8'
    #     if '太频繁' in response.text:
    #         print(response.text)
    #         self.lagou_session.cookies.clear()
    #         first_request_url = "https://www.lagou.com/jobs/list_python?city=%s&cl=false&" \
    #                             "fromSearch=true&labelWords=&suginput=" % info
    #         self.handle_request(url=first_request_url, method='GET')
    #         time.sleep(10)
    #         continue
    #     return response.text


if __name__ == '__main__':
    la_gou = HandelLaGou()
    la_gou.handel_city()
    # # 多进程方式
    # pool = multiprocessing.Pool(2)
    # for city in la_gou.city_list:
    #     pool.apply_async(la_gou.handle_city_job, args=city)

    # for city in la_gou.city_list:
    #     # print(city)
    #     la_gou.handle_city_job(city)
    #     break
    la_gou.handle_city_job('上海')