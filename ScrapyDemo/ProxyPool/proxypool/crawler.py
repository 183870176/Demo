import json
import re
from .utils import get_page
from pyquery import PyQuery as pq


class ProxyMetaclass(type):
    def __new__(cls, name, bases, attrs):
        count = 0
        attrs['__CrawlFunc__'] = []
        for k, v in attrs.items():
            if 'crawl_' in k:
                attrs['__CrawlFunc__'].append(k)
                count += 1
        attrs['__CrawlFuncCount__'] = count
        return type.__new__(cls, name, bases, attrs)


class Crawler(object, metaclass=ProxyMetaclass):
    def get_proxies(self, callback):
        proxies = []
        for proxy in eval("self.{}()".format(callback)):
            print('成功获取到代理', proxy)
            proxies.append(proxy)
        return proxies
        
    # def crawl_daxiang(self):
    #     url = 'http://vtp.daxiangdaili.com/ip/?tid=559363191592228&num=50&filter=on'
    #     html = get_page(url)
    #     if html:
    #         urls = html.split('\n')
    #         for url in urls:
    #             yield url






    def crawl_ip3366(self):
        for page in range(1, 4):
            start_url = 'http://www.ip3366.net/free/?stype=1&page={}'.format(page)
            html = get_page(start_url)
            ip_address = re.compile('<tr>\s*<td>(.*?)</td>\s*<td>(.*?)</td>')
            re_ip_address = ip_address.findall(html)
            for address, port in re_ip_address:
                result = address+':'+ port
                yield result.replace(' ', '')

    # def crawl_premproxy(self):
    #     for i in ['China-01','China-02','China-03','China-04','Taiwan-01']:
    #         start_url = 'https://premproxy.com/proxy-by-country/{}.htm'.format(i)
    #         html = get_page(start_url)
    #         if html:
    #             ip_address = re.compile('<td data-label="IP:port ">(.*?)</td>')
    #             re_ip_address = ip_address.findall(html)
    #             for address_port in re_ip_address:
    #                 yield address_port.replace(' ','')
    #
    # def crawl_xroxy(self):
    #     for i in ['CN','TW']:
    #         start_url = 'http://www.xroxy.com/proxylist.php?country={}'.format(i)
    #         html = get_page(start_url)
    #         if html:
    #             ip_address1 = re.compile("title='View this Proxy details'>\s*(.*).*")
    #             re_ip_address1 = ip_address1.findall(html)
    #             ip_address2 = re.compile("title='Select proxies with port number .*'>(.*)</a>")
    #             re_ip_address2 = ip_address2.findall(html)
    #             for address,port in zip(re_ip_address1,re_ip_address2):
    #                 address_port = address+':'+port
    #                 yield address_port.replace(' ','')
    
    def crawl_kuaidaili(self):
        for i in range(1, 4):
            start_url = 'http://www.kuaidaili.com/free/inha/{}/'.format(i)
            html = get_page(start_url)
            if html:
                ip_address = re.compile('<td data-title="IP">(.*?)</td>') 
                re_ip_address = ip_address.findall(html)
                port = re.compile('<td data-title="PORT">(.*?)</td>')
                re_port = port.findall(html)
                for address,port in zip(re_ip_address, re_port):
                    address_port = address+':'+port
                    yield address_port.replace(' ','')

    def crawl_xicidaili(self):
        for i in range(1, 4):
            start_url = 'http://www.xicidaili.com/nn/{}'.format(i)
            headers = {
                'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
                'Cookie':'_free_proxy_session=BAh7B0kiD3Nlc3Npb25faWQGOgZFVEkiJWRjYzc5MmM1MTBiMDMzYTUzNTZjNzA4NjBhNWRjZjliBjsAVEkiEF9jc3JmX3Rva2VuBjsARkkiMUp6S2tXT3g5a0FCT01ndzlmWWZqRVJNek1WanRuUDBCbTJUN21GMTBKd3M9BjsARg%3D%3D--2a69429cb2115c6a0cc9a86e0ebe2800c0d471b3',
                'Host':'www.xicidaili.com',
                'Referer':'http://www.xicidaili.com/nn/3',
                'Upgrade-Insecure-Requests':'1',
            }
            html = get_page(start_url, options=headers)
            if html:
                find_trs = re.compile('<tr class.*?>(.*?)</tr>', re.S)
                trs = find_trs.findall(html)
                for tr in trs:
                    find_ip = re.compile('<td>(\d+\.\d+\.\d+\.\d+)</td>') 
                    re_ip_address = find_ip.findall(tr)
                    find_port = re.compile('<td>(\d+)</td>')
                    re_port = find_port.findall(tr)
                    for address,port in zip(re_ip_address, re_port):
                        address_port = address+':'+port
                        yield address_port.replace(' ','')
    
    def crawl_ip3366(self):
        for i in range(1, 4):
            start_url = 'http://www.ip3366.net/?stype=1&page={}'.format(i)
            html = get_page(start_url)
            if html:
                find_tr = re.compile('<tr>(.*?)</tr>', re.S)
                trs = find_tr.findall(html)
                for s in range(1, len(trs)):
                    find_ip = re.compile('<td>(\d+\.\d+\.\d+\.\d+)</td>')
                    re_ip_address = find_ip.findall(trs[s])
                    find_port = re.compile('<td>(\d+)</td>')
                    re_port = find_port.findall(trs[s])
                    for address,port in zip(re_ip_address, re_port):
                        address_port = address+':'+port
                        yield address_port.replace(' ','')
    
    # def crawl_iphai(self):
    #     start_url = 'http://www.iphai.com/'
    #     html = get_page(start_url)
    #     if html:
    #         find_tr = re.compile('<tr>(.*?)</tr>', re.S)
    #         trs = find_tr.findall(html)
    #         for s in range(1, len(trs)):
    #             find_ip = re.compile('<td>\s+(\d+\.\d+\.\d+\.\d+)\s+</td>', re.S)
    #             re_ip_address = find_ip.findall(trs[s])
    #             find_port = re.compile('<td>\s+(\d+)\s+</td>', re.S)
    #             re_port = find_port.findall(trs[s])
    #             for address,port in zip(re_ip_address, re_port):
    #                 address_port = address+':'+port
    #                 yield address_port.replace(' ','')


            