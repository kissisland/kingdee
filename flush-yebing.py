import requests
from multiprocessing.dummy import Pool
import xmltodict
import time


def flush_page(url):
    try:
        res = requests.get(url, timeout=5)
        if res.status_code == 200:
            print("刷新成功")
        else:
            flush_page(url)
            time.sleep(5)
    except Exception as e:
        print(e)
        time.sleep(5)
        flush_page(url)


def search_sitemaplink():
    doc = xmltodict.parse(requests.get("https://www.yebing.cn/sitemap.xml").text)
    urls = [url['loc'] for url in doc['sitemapindex']['sitemap']][1:]
    all_url = []
    for url in urls:
        doc = xmltodict.parse(requests.get(url).text)
        for i in doc['urlset']['url']:
            all_url.append(i['loc'])
            flush_page(i['loc'])

    return all_url


if __name__ == '__main__':

    search_sitemaplink()