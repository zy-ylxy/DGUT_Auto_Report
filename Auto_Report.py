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


def pop_dict(data: dict, pop_list: list):
    pop_items = []
    for i in data.keys():
        if i in pop_list:
            pop_items.append(i)
    for i in pop_items:
        data.pop(i)
    return data


if __name__ == "__main__":
    try:
        # 1、输入账号密码
        username = sys.argv[1]
        password = sys.argv[2]

        # 2、监控时间，启动程序
        while True:
            if (datetime.datetime.utcnow() + datetime.timedelta(hours=8)).hour == 0 and (datetime.datetime.utcnow() + datetime.timedelta(hours=8)).minute >= 10:
                break
            time.sleep(60)

        # 3、创建用户类
        u = DgutLogin(username, password)

        # 4、登录用户并获取access_token
        response = u.signin('illness')
        if response['code'] == 400:
            exit(u.login['illness']['response'][0][1].text)
        while response['code'] != 1:
            time.sleep(5)
            u = DgutLogin(username, password)
            response = u.signin('illness')

        access_token = re.search(
            r'access_token=(.*)', u.login['illness']['response'][0][2].url, re.S)
        if not access_token:
            exit("获取access_token失败")
        access_token = access_token.group(1)
        headers = {
            'authorization': 'Bearer ' + access_token,
            'Host': 'yqfk.dgut.edu.cn',
            'Referer': 'https://yqfk.dgut.edu.cn/main',
        }

        # 5、获取并修改数据
        count = 1
        response = u.session.get(
            'https://yqfk.dgut.edu.cn/home/base_info/getBaseInfo', headers=headers)
        while json.loads(response.text)['code'] != 200 and count < 20:
            time.sleep(5)
            response = u.session.get(
                'https://yqfk.dgut.edu.cn/home/base_info/getBaseInfo', headers=headers)
            count += 1
        if json.loads(response.text)['code'] != 200:
            exit("获取个人基本信息失败")
        data = json.loads(response.text)['info']
        pop_list = [
            'can_submit',
            'class_id',
            'class_name',
            'continue_days',
            'create_time',
            'current_area',
            'current_city',
            'current_country',
            'current_district',
            'current_province',
            'faculty_id',
            'faculty_name',
            'id',
            'msg',
            'name',
            'username',
            'whitelist',
            'importantAreaMsg',
        ]
        data = pop_dict(data, pop_list)
        data['important_area'] = None
        data['current_region'] = None
        # for key, value in data.items():
        #     print(f"{key}: {value}")

        # 6、提交数据
        count = 1
        response = u.session.post(
            "https://yqfk.dgut.edu.cn/home/base_info/addBaseInfo", headers=headers, json=data)
        result = json.loads(response.text)
        print(response)
        print(response.text)
        while (result['code'] not in [200, 400] or (result['code'] == 200 and result['info'] != 0)) and count < 200:
            time.sleep(5)
            response = u.session.post(
                "https://yqfk.dgut.edu.cn/home/base_info/addBaseInfo", headers=headers, json=data)
            result = json.loads(response.text)
            count += 1
            print(response)
            print(response.text)
        if count >= 200:
            print("打卡失败")

    except IndexError:
        print("请完整输入账号、密码和提交的表单")
    except json.decoder.JSONDecodeError:
        print("json解析错误")
