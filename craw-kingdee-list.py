import requests
import pymongo
import re
import time
from baidu_sumary import get_summary

client = pymongo.MongoClient()
kingdee = client['kingkee']
article = kingdee['article']


base_url = "http://www.kingdee.com/kdsource/public/index.php/column/tagArticleList/8?page={}"


def clean_content(content):
    content = re.sub(r'<p[^>]*?>', '', content)
    content = re.sub(r'</p[^>]*?>', '', content)
    content = re.sub(r'<div[^>]*?>', '', content)
    content = re.sub(r'</div[^>]*?>', '', content)
    content = re.sub(r'</div[^>]*?>', '', content)
    content = re.sub(r'<img[^>]*?>', '', content)
    return content


def clean_html(content, title):
    content = re.sub(r'<(?!p|b|/b|span|/span|img|/p|div|/div)[^<>]*?>', '', content).strip()
    content = re.sub(r'<p[^>]*?>', '<p>', content)
    content = re.sub(r'<span[^>]*?>', '<span>', content)
    content = re.sub(r'<div[^>]*?>', '<div>', content)
    img = re.search('img.*?src="(.*?)"', content, re.S)
    img = img.group(1) if img else ''
    if "http" in img:
        text = '<p style="text-align: center;"><img src="{}"  alt="{}" title="{}" /></p>'
        text = text.format(img, title, title)
    elif 'png' in img or 'jpg' in img:
        text = '<p style="text-align: center;"><img src="http://www.kingdee.com/{}"  alt="{}" title="{}" /></p>'
        text = text.format(img, title, title)
    else:
        text = content
    # print(text)
    content = re.sub(r'<p><img[^>]*?>.*?</p>', text, content)
    # content = re.sub(r'title="(.*?)\.(png|jpg|jpeg)"', 'title="{}"'.format(title), content)
    return content


def url_list(page):
    res = requests.get(base_url.format(page))
    seletor = res.json()

    datas = seletor['data']

    for data in datas:
        info = {
            "title": data.get("title"),
            "content": clean_html(data.get("content"), data.get("title")),
            # "content":data.get("content"),
            "keyword": data.get("keyword"),
            'url': data.get("url"),
            'date': data.get("created_at"),
            'status': 0
        }
        if "金蝶" not in info['title'] and '精斗云' not in info['title']:
            if article.count_documents({'url': info['url']}) <= 0:
                article.insert_one(info)
                print(info)


def get_imgs(content, url):
    img = re.search('img.*?src="(.*?)"', content, re.S)
    img = img.group(1) if img else ''
    img_url = img
    img_name = img.split('/')[-1]

    try:
        pass
        res = requests.get(img_url, timeout=8)
        if res.status_code == 200:
            img = res.content
            open('{}'.format(img_name), 'wb').write(img)
        else:
            file = open("err.txt", 'a', encoding='utf-8')
            file.write(url)
            file.write('\n')
    except Exception as e:
        print(e)
        file = open("err.txt", 'a', encoding='utf-8')
        file.write(url)
        file.write('\n')
        print(img_url)


if __name__ == '__main__':

    # for i in range(1, 20):
    #     url_list(i)
    #     time.sleep(1)

    # 删除没有status的
    # for item in article.find():
    #     if item.get("status"):
    #         pass
    #     else:
    #         article.delete_one({'_id': item.get("_id")})

    for item in article.find({'status': 0}):
        # 下载图片
        # get_imgs(item['content'], item['url'])

        # 添加百度自动摘要200字
        # try:
        #     article.update_one({"_id": item['_id']}, {"$set": {'summary': get_summary(clean_content(str(item['content']).encode('gbk', 'ignore').decode('gbk')))}})
        # except Exception as e:
        #     print(e)


        # 处理图片问题
        # if "http://www.kingdee.com/kdsource/public" in item['content']:
        #     img = re.search('img src="(.*?)"', item['content'], re.S)
        #     img = img.group(1).strip() if img else item['url']
        #     img_url = img
        #     img_name = img.split('/')[-1]
        #     newcontent = item['content'].replace(img_url, "{}/{}".format("https://www.yebing.cn/wp-content/uploads/kingimgs", img_name))
        #     print(newcontent)
        #     article.update_one({"_id": item['_id']}, {"$set": {'content': newcontent}})
        #
        #     print(item)

        # 清理图片中的哼唧
        newcontent = clean_html(item['content'], item['title'])
        article.update_one({"_id": item['_id']}, {"$set": {'content': newcontent}})
