from wordpress_xmlrpc import Client, WordPressPost
from wordpress_xmlrpc import ServerConnectionError
from wordpress_xmlrpc.methods import posts
from datetime import datetime, timedelta
import csv
import time
import random
from pymongo import MongoClient
import requests

conn = MongoClient()
kingkee = conn['kingkee']
article = kingkee['article']

kuaijiwang = conn['kuaijiwang']
kuaijiwangurllist = kuaijiwang['urllist']
kuaijiwangarticle = kuaijiwang['article']


# article_list = kjkp_data['article_list'] #会计实务
# article_detail = kjkp_data['article_detail'] #会计实务
#
#
# shuiwu_list = kjkp_data['shuiwu_list'] #会计税务
# shuiwu_detail = kjkp_data['shuiwu_detail'] #会计税务

fenlei_catgory = {
                'yc': ['财务考试'],
                'kuaijishiwu': ['会计税务'],
                'cpa': ['注册会计师', '财务考试'],
                'cjkjzc': ['初级会计考试职称', '财务考试'],
                'zjkjzc': ['中级会计考试职称', '财务考试'],
                'shuiwushi': ['税务师', '财务考试'],
                'xinwen': ['会计实务'],
                'cfa': ['CFA', '财务考试'],
                'cma': ['CMA', '财务考试'],
                'acca': ['ACCA', '财务考试'],
                'qihuocongye': ['期货从业', '财务考试'],
                'frm': ['FRM', '财务考试'],
                'cia': ['CIA', '财务考试'],
                'zqcy': ['证券从业', '财务考试'],
                'jijincongye': ['基金从业', '财务考试'],
                'zjsjs': ['中级审计师', '财务考试'],
                'zgglkjscj': ['中国管理会计师（初级）', '财务考试'],   # 这里未录入
                'gjkjzc': ['高级会计职称', '财务考试'],
                'uscpa': ['USCPA', '财务考试'],
                'yxcy': ['银行从业', '财务考试'],
                'jingsuanshi': ['精算师', '财务考试'],
                'cjsjs': ['初级审计师', '财务考试'],
                'caia': ['CAIA', '财务考试'],
                'zcpgs': ['资产评估师', '财务考试'],
                'zgglkjszj': ['中国管理会计师（中级）', '财务考试'],
                'cwm': ['CWM', '财务考试'],
                'cima': ['CIMA', '财务考试'],
                'tongjishi': ['统计师', '财务考试'],
                'afp': ['AFP', '财务考试'],
                'mpacc': ['MPACC', '财务考试'],
                'cqf': ['CQF', '财务考试'],
                'rfc': ['RFC', '财务考试'],
                'gjsjs': ['高级审计师', '财务考试'],
                'aca': ['ACA', '财务考试'],
                'ciia': ['CIIA', '财务考试'],
                'cfrm': ['CFRM', '财务考试'],
                'aia': ['AIA', '财务考试'],
                'rfp': ['RFP', '财务考试'],
                'ccsa': ['RFP', '财务考试'],
                'jianadacpa': ['加拿大CPA', '财务考试'],
                'aozhoucpa': ['澳洲CPA', '财务考试'],
                'hkicpa': ['HKICPA', '财务考试'],
                'cfp': ['CFP', '财务考试'],
            }


def flush(url):
    res = requests.get(url).text


def push_wp():
    try:  # 检测是否登录成功
        # 登录WordPress后台
        client = Client("https://www.yebing.cn/xmlrpc.php", "yebing", "yeye910103")
    except ServerConnectionError:
        print('登录失败')
    else:
        print('登录成功')

        # wp = client.call(posts.GetPosts({'orderby': 'post_modified', 'number': 50}))
        # for w in wp:
        #     print(w.link)

        for item in article.find({"status": 0}):
            # NewPost()方法，新建一篇文章
            newpost = WordPressPost()  # 创建一个类实例，注意，它不是一个函数。只要在一个类名后面加上括号就是一个实例
            newpost.title = item['title']
            newpost.content = item['content']
            newpost.excerpt = item['summary']

            newpost.post_status = 'draft'  # private表示私密的，draft表示草稿，publish表示发布
            newpost.comment_status = "open"

            newpost.terms_names = {'post_tag': item['keyword'].split(","),  # 文章所属标签，没有则自动创建
                                   'category': ["会计实务"]}  # 文章所属分类，没有则自动创建}
            print(item['keyword'].split(","))
            time.sleep(random.randint(30, 80))

            aid = client.call(posts.NewPost(newpost))
            if aid:
                article.update_one({'_id': item['_id']}, {'$set': {'status': 1}})
                print(aid)  # 发布新建的文章，返回的是文章id


def push_kuaijiwang():
    try:  # 检测是否登录成功
        # 登录WordPress后台
        client = Client("https://www.yebing.cn/xmlrpc.php", "yebing", "yeye910103")
    except ServerConnectionError:
        print('登录失败')
    else:
        print('登录成功')

        # wp = client.call(posts.GetPosts({'orderby': 'post_modified', 'number': 50}))
        # for w in wp:
        #     print(w.link)

        for item in kuaijiwangarticle.find({"status": 0}):

            if item['fenlei'] in fenlei_catgory.keys():

                if item['tags'].split(",")[0]:  # 判断是否有标签，有标签的直接发布，没有的手工

                    # NewPost()方法，新建一篇文章
                    newpost = WordPressPost()  # 创建一个类实例，注意，它不是一个函数。只要在一个类名后面加上括号就是一个实例
                    newpost.title = item['title']
                    newpost.content = item['content']
                    newpost.excerpt = item['summay']

                    newpost.post_status = 'publish'  # private表示私密的，draft表示草稿，publish表示发布
                    newpost.comment_status = "open"

                    newpost.terms_names = {'post_tag': item['tags'].split(",")[:2],  # 文章所属标签，没有则自动创建
                                           'category': fenlei_catgory.get(item['fenlei'])}  # 文章所属分类，没有则自动创建}
                    time.sleep(random.randint(30, 120))

                    aid = client.call(posts.NewPost(newpost))
                    if aid:
                        kuaijiwangarticle.update_one({'_id': item['_id']}, {'$set': {'status': 1}})
                        ar_url = "https://www.yebing.cn/article_{}.html".format(aid)
                        print(ar_url)
                        flush(ar_url)


if __name__ == '__main__':
    # editdata(4539)

    # push_wp()

    push_kuaijiwang()
