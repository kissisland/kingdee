from aip import AipNlp

""" 你的 APPID AK SK """
APP_ID = '16180158'
API_KEY = 'nERfNUG22msrAxmkwhveFxyD'
SECRET_KEY = 'WvhrzIvfKi7doreNBImSBgvrKqwSF7h2'


def get_tags(title, content):

    client = AipNlp(APP_ID, API_KEY, SECRET_KEY)

    """ 调用文章标签 """
    data = client.keyword(title, content)
    data = data['items']
    data = [i['tag'] for i in data][:2]
    data = ','.join(data)
    return data


if __name__ == '__main__':

    print(get_tags("拆迁补偿怎么开票？", "营改增后被拆迁企业取得拆迁补偿如何开票?以下是有关营改增后被拆迁企业取得拆迁补偿如何开票等等的介绍"))
