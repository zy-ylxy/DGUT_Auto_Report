# coding:utf-8
from Dgut.DgutLogin import DgutLogin
import re
import json
import datetime
import sys
import time

try:
    username = sys.argv[1]
    password = sys.argv[2]
    # data = json.loads(sys.argv[3])
    print(username)
    print(sys.argv[3])
    print(type(sys.argv[3]))
    # while True:
    #     if (datetime.datetime.utcnow() + datetime.timedelta(hours=8)).hour == 0 and (datetime.datetime.utcnow() + datetime.timedelta(hours=8)).minute >= 20:
    #         break
    #     time.sleep(60)

    # 获取当日时间，修改字典
    # now = datetime.datetime.utcnow() + datetime.timedelta(hours=8)
    # data['submit_time'] = now.strftime("%Y-%m-%d")

    # count = 1
    # while True:
    #     u = DgutLogin(username, password)
    #     u.timeout = 30

    #     # 登录
    #     response = u.signin('illness')
    #     print(response)

    #     # 获取access_token
    #     access_token = re.search(
    #         r'access_token=(.*)', u.login['illness']['response'][0][2].url, re.S).group(1)
    #     print(f"access_token={access_token}")

    #     # 构造headers
    #     headers = {
    #         'authorization': 'Bearer ' + access_token,
    #         'Host': 'yqfk.dgut.edu.cn',
    #         'Referer': 'https://yqfk.dgut.edu.cn/main',
    #     }

    #     # 提交
    #     response = u.session.post(
    #         "https://yqfk.dgut.edu.cn/home/base_info/addBaseInfo", headers=headers, json=data)
    #     print("-"*20 + "结果" + "-"*20)
    #     print(response)
    #     print(response.text)
    #     if response.status_code == 200:
    #         break
    #     if count > 10:
    #         print("打卡失败")
    #         raise Exception
    #     time.sleep(60*5)
except IndexError:
    print("请完整输入账号、密码和提交的表单")
except json.decoder.JSONDecodeError:
    print("json解析错误")
