# coding:utf-8
from Dgut.DgutLogin import DgutLogin
import re
import json
import datetime
import sys
import time


def Merge(dict1, dict2):
    '''
    合并两个字典
    '''
    res = {**dict1, **dict2}
    return res


if __name__ == "__main__":
    try:
        username = sys.argv[1]
        password = sys.argv[2]

        card_number, tel, connect_person, connect_tel, family_address_detail = sys.argv[3].split(
            ",")
        form1 = {
            'card_number': card_number,
            'tel': tel,
            'connect_person': connect_person,
            'connect_tel': connect_tel,
            'family_address_detail': family_address_detail,
        }

        fp = open("./data.json", 'rb')
        form2 = json.loads(fp.read())
        data = Merge(form1, form2)

        # while True:
        #     if (datetime.datetime.utcnow() + datetime.timedelta(hours=8)).hour == 0 and (datetime.datetime.utcnow() + datetime.timedelta(hours=8)).minute >= 20:
        #         break
        #     time.sleep(60)

        # 获取当日时间，修改字典
        now = datetime.datetime.utcnow() + datetime.timedelta(hours=8)
        data['submit_time'] = now.strftime("%Y-%m-%d")

        count = 1
        while True:
            u = DgutLogin(username, password)
            u.timeout = 30

            # 登录
            for i in range(3):
                response = u.signin('illness')
                print(response['message'])
                if response['code'] == 1:
                    break
                time.sleep(30)

            # 获取access_token
            access_token = re.search(
                r'access_token=(.*)', u.login['illness']['response'][0][2].url, re.S).group(1)
            if not access_token:
                print("获取access_token失败")
                raise Exception

            # 构造headers
            headers = {
                'authorization': 'Bearer ' + access_token,
                'Host': 'yqfk.dgut.edu.cn',
                'Referer': 'https://yqfk.dgut.edu.cn/main',
            }

            # 提交
            response = u.session.post(
                "https://yqfk.dgut.edu.cn/home/base_info/addBaseInfo", headers=headers, json=data)
            print("-"*20 + "结果" + "-"*20)
            print(response)
            print(response.text)
            if json.loads(response.text)['code'] in [200, 400]:
                break
            if count > 10:
                print("打卡失败")
                raise Exception
            time.sleep(60*5)
    except IndexError:
        print("请完整输入账号、密码和提交的表单")
    except json.decoder.JSONDecodeError:
        print("json解析错误")
