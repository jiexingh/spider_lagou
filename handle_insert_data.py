"""
create by jxh @2019/6/28
"""
from lagou_table import LaGouTable, Session
import time


class HandleLaGouData(object):
    def __init__(self):
        self.my_session = Session()

    def inset_item(self, item):
        date = time.strftime('%Y-%m-%d', time.localtime())
        # 存储的数据结构
        data = LaGouTable(
            # 岗位ID
            positionID=item['positionId'],
            # 经度
            longitude=item['longitude'],
            # 纬度
            latitude=item['latitude'],
            # 岗位名称
            positionName=item['positionName'],
            # 工作年限
            workYear=item['workYear'],
            # 学历
            education=item['education'],
            # 岗位性质
            jobNature=item['jobNature'],
            # 公司类型
            financeStage=item['financeStage'],
            # 公司规模
            companySize=item['companySize'],
            # 业务方向
            industryField=item['industryField'],
            # 所在城市
            city=item['city'],
            # 岗位标签
            positionAdvantage=item['positionAdvantage'],
            # 公司简称
            companyShortName=item['companyShortName'],
            # 公司全称
            companyFullName=item['companyFullName'],
            # 公司所在区
            district=item['district'],
            # 公司福利标签
            companyLabelList=','.join(item['companyLabelList']),
            salary=item['salary'],
            # 抓取日期
            crawl_date=date
        )

        # 查询是否拥有岗位信息
        query_result = self.my_session.query(LaGouTable).filter(LaGouTable.crawl_date == date,
                                                                LaGouTable.positionID == item['positionId']
                                                                ).first()
        if query_result:
            print('该岗位信息已存在%s:%s:%s'%(item['positionId'], item['city'], item['positionName']))
        else:
            self.my_session.add(data)
            self.my_session.commit()
            print('新增岗位信息%s'%item['positionId'])


la_gou_mysql = HandleLaGouData()
