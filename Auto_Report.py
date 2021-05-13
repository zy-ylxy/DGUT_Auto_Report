import click
from dgut_requests.dgut import *


class dgutIll(dgutUser):
    def __init__(self, username: str, password: str):
        dgutUser.__init__(self, username, password)
        self.session.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.141 Safari/537.36',
            'Host': 'yqfk.dgut.edu.cn',
        }

    @decorator_signin(illness_login)
    def report(self):
        # 1、获取access_token
        response = self.signin(illness_login)
        access_token = re.search(
            r'access_token=(.*)', response.url, re.S)
        if not access_token:
            raise AuthError("获取access_token失败")
        access_token = access_token.group(1)
        self.session.headers['authorization'] = 'Bearer ' + access_token

        # GPS
        response = self.session.get(
            "https://yqfk.dgut.edu.cn/home/base_info/getGPSAddress?longitude=113.87651&latitude=22.90701&reject=1")
        print("GPS:")
        print(response, response.text)

        # 2、获取并修改数据
        response = self.session.get(
            'https://yqfk.dgut.edu.cn/home/base_info/getBaseInfo')
        if json.loads(response.text)['code'] != 200:
            raise AuthError("获取个人基本信息失败")
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
        for key in pop_list:
            if data.get(key):
                data.pop(key)

        # 3、提交数据
        response = self.session.post(
            "https://yqfk.dgut.edu.cn/home/base_info/addBaseInfo", json=data)
        return json.loads(response.text)


@click.command()
@click.option('-U', '--username', required=True, help="中央认证账号用户名", type=str)
@click.option('-P', '--password', required=True, help="中央认证账号密码", type=str)
def main(username, password):
    users = username.split(",")
    pwds = password.split(",")
    if len(users) != len(pwds):
        exit("账号和密码个数不一致")
    for usr in zip(users, pwds):
        u = dgutIll(usr[0], usr[1])
        print(u.report())


if __name__ == '__main__':
    main()
