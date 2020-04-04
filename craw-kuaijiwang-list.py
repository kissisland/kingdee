import requests
import pymongo
import re
from lxml import etree
from urllib.parse import urljoin
import time
import random
from baidu_sumary import get_summary
from tags import get_tags
from collections import Counter

client = pymongo.MongoClient()
kuaijiwang = client['kuaijiwang']
urllist = kuaijiwang['urllist']
article = kuaijiwang['article']

domain_url = "https://www.kuaiji.com/"
yc_base_url = "https://www.kuaiji.com/yc/"

fenlei_url_list = ['https://www.kuaiji.com/xinwen/', 'https://www.kuaiji.com/kaoshi/', "https://www.kuaiji.com/yc/"]

fenlei_tags = {
                'cpa': ['注册会计师', 'cpa'],
                'cjkjzc': ['初级会计', '初级会计考试', '初级会计考试职称'],
                'zjkjzc': ['中级会计', '中级会计考试', '中级会计考试职称'],
                'shuiwushi': ['税务师', '税务师考试'],
                'cfa': ['CFA', 'CFA考试'],
                'cma': ['CMA', 'CMA考试'],
                'acca': ['ACCA', 'ACCA考试'],
                'qihuocongye': ['期货从业'],
                'frm': ['FRM', 'FRM考试'],
                'cia': ['CIA', 'CIA考试'],
                'zqcy': ['证券从业'],
                'jijincongye': ['基金从业'],
                'zjsjs': ['中级审计师'],
                'zgglkjscj': ['中国管理会计师（初级）'],   # 这里未录入
                'gjkjzc': ['高级会计', '高级会计职称'],
                'uscpa': ['USCPA', 'USCPA考试'],
                'yxcy': ['银行从业'],
                'jingsuanshi': ['精算师'],
                'cjsjs': ['初级审计师'],
                'caia': ['CAIA', 'CAIA考试'],
                'zcpgs': ['资产评估师'],
                'zgglkjszj': ['中国管理会计师（中级）'],
                'cwm': ['CWM', 'CWM考试'],
                'cima': ['CIMA', 'CIMA考试'],
                'tongjishi': ['统计师'],
                'afp': ['AFP', 'AFP考试'],
                'mpacc': ['MPACC', 'MPACC考试'],
                'cqf': ['CQF', 'CQF考试'],
                'rfc': ['RFC', 'RFC考试'],
                'gjsjs': ['高级审计师'],
                'aca': ['ACA', 'ACA考试'],
                'ciia': ['CIIA', 'CIIA考试'],
                'cfrm': ['CFRM', 'CFRM考试'],
                'aia': ['AIA', 'AIA考试'],
                'rfp': ['RFP', 'RFP考试'],
                'ccsa': ['RFP', 'RFP考试'],
                'jianadacpa': ['加拿大CPA'],
                'aozhoucpa': ['澳洲CPA'],
                'hkicpa': ['HKICPA'],
                'cfp': ['CFP', 'CFP考试'],
            }


def clean_content(content):
    content = re.sub(r'<p[^>]*?>', '', content)
    content = re.sub(r'</p[^>]*?>', '', content)
    content = re.sub(r'<br/>', '', content)
    content = re.sub(r'<div[^>]*?>', '', content)
    content = re.sub(r'</div[^>]*?>', '', content)
    content = re.sub(r'</div[^>]*?>', '', content)
    content = re.sub(r'<img[^>]*?>', '', content)
    content = re.sub(r'<strong[^>]*?>', '', content)
    content = re.sub(r'</strong[^>]*?>', '', content)
    content = re.sub(r'</span>', '', content)
    content = re.sub(r'<span>', '', content)
    content = re.sub(r'　　', '', content)
    content = re.sub(r'&#.*?;', '', content)

    return content


def clean_html(content):
    content = re.sub(r'<(?!p|b|/b|span|/span|img|/p|strong|/strong|div|/div)[^<>]*?>', '', content).strip()
    content = re.sub(r'<p[^>]*?>', '<p>', content)
    content = re.sub(r'<span[^>]*?>', '<span>', content)
    content = re.sub(r'<div[^>]*?>', '<div>', content)
    content = re.sub(r'<p><img[^>]>.*?</p>', "", content)
    content = re.sub(r'<img[^>]*?>', "", content)
    content = re.sub(r'<p></p>', "", content)
    content = content.lstrip('<div class="article-body">').strip()
    content = content.rstrip("</div>").strip()
    content = re.sub(r'&#.*?;', '', content)
    content = content.replace('会计网', '夜冰会计网校')

    return content


def url_list(list_url, page):
    if page == 1:
        res = requests.get(list_url)
    else:
        res = requests.get("{}{}.html".format(list_url, page))
    res.encoding = res.apparent_encoding
    html = res.text
    seletor = etree.HTML(html)

    for data in seletor.xpath("//div[@class='left']/div[@class='list-cont']/ul/li/div[@class='list-intro']/div[@class='list-name']"):
        title = data.xpath("a/text()")
        title = title[0] if title else ''
        link = data.xpath("a/@href")
        link = link[0] if link else ''
        link = urljoin(domain_url, link)

        fenlei = link.replace("https://www.kuaiji.com", '').split('/')[1]

        if urllist.count_documents({'link': link}) <= 0:
            urllist.insert_one({
                'title': title,
                'link': link,
                'status': 0,
                'fenlei': fenlei
            })

            print(title, link)


def get_list_data(list_url, spage, epage):
    # 遍历列表页
    for i in range(spage, epage):
        url_list(list_url, i)
        time.sleep(random.randint(1, 3))


def get_all_list_data(spage, epage):

    for url in fenlei_url_list:
        get_list_data(url, spage, epage)


def get_detail(detailurl, fenlei):

    try:
        res = requests.get(detailurl)
        res.encoding = res.apparent_encoding
        selector = etree.HTML(res.text)
        title = selector.xpath("//div[@class='article-head']/h2/text()")
        title = title[0] if title else ''
        content = selector.xpath("//div[@class='article']/div[@class='article-body']")
        content = etree.tostring(content[0], encoding='utf-8').decode()
        content = clean_html(content)
        summary = clean_content(content)
        summary = get_summary(summary)

        if "违者将被依法追究法律责任" not in content:

            tag = fenlei_tags.get(fenlei, '[]')
            tag.extend(get_tags(title, content))
            tag = set(tag)
            tag = ','.join(tag)

            if article.count_documents({'link': detailurl}) <= 0:
                article.insert_one({
                    'title': title,
                    'content': content,
                    'summay': summary,
                    'link': detailurl,
                    'tags': tag,
                    'status': 0,
                    'fenlei': fenlei
                })
            else:
                print("链接重复")
            print(title)
    except Exception as e:
        pass


if __name__ == '__main__':

    # get_all_list_data(1, 8)
    #
    # # 从列表页中采集文章
    # for item in urllist.find({'status': 0}):
    #     try:
    #         get_detail(item['link'], item['fenlei'])
    #     except Exception as e:
    #         print(e)
    #     else:
    #         urllist.update_one({'_id': item['_id']}, {"$set": {'status': 1}})

    # 查询内容中的分类内容数量
    fenlei_title = Counter([i['fenlei'] for i in article.find({'status': 0})])
    print(fenlei_title)
    print(len([i['fenlei'] for i in article.find({'status': 0})]))

    # for item in article.find({'status': 0}):
        # 关键词处理
        # if "违者将被依法追究法律责任" in item['content']:
        #     article.update_one({'_id': item['_id']}, {"$set": {'status': 1}})
        #     print(item['content'])

        # article.update_one({'_id': item['_id']}, {"$set": {'summay': clean_content(item['summay'])}})
