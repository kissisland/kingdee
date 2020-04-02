from aip import AipNlp

""" 你的 APPID AK SK """
APP_ID = '16180158'
API_KEY = 'nERfNUG22msrAxmkwhveFxyD'
SECRET_KEY = 'WvhrzIvfKi7doreNBImSBgvrKqwSF7h2'

def get_summary(content):

    client = AipNlp(APP_ID, API_KEY, SECRET_KEY)

    maxSummaryLen = 200

    """ 调用新闻摘要接口 """
    client.newsSummary(content, maxSummaryLen);

    """ 如果有可选参数 """
    options = {}
    options["title"] = "标题"

    """ 带参数调用新闻摘要接口 """

    data = client.newsSummary(content, maxSummaryLen)
    data = data.get("summary")
    return data

if __name__ == '__main__':
    item = """
什么是增值税专用发票？

增值税专用发票是反映经济活动的重要会计凭证，也是卖方纳税义务和买方进入税的法律证明。在增值税的计算和管理中，它是一种重要的、决定性的法定专用发票。关键是只有一般纳税人才能收到并使用它作为扣除投入产出税的凭证。

增值税专用发票与普通发票有以下区别：

1、主体不同:

增值税专用发票限于一般纳税人对增值税的使用。需要小规模纳税人使用的，经税务机关批准后，由税务机关开户；普通发票的税务人员可以使用。

2、内容不同：

增值税专用发票包括发票单位、收款人、开票日期、采购单位、销售单位、单价、价格，普通发票也包括税务登记号，但不包括增值税税额、适用税率、应交增值税税额等。

3、作用不同:

增值税专用发票既是买卖双方的付款凭证，又是买方扣除增值税的凭证，普通发票只能按照法定的运费、农副产品和废弃物税率扣除。

4、印制不同:

增值税专用发票在国家税务总局监督下设计印制，普通发票由省、自治区、直辖市和地方税务局按照国务院主管部门的规定指定。

5、联次不同:

增值税专用发票四次七次，普通发票三次。

虽然普通纳税人有权开具特殊的增值税发票，享有扣除的“特权”，但小规模纳税人也具有税率低的优势，需要根据自己的实际情况选择最合适的纳税人身份。
"""
    print(get_summary(item))