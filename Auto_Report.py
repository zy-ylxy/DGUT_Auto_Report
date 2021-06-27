import click
from dgut_requests.dgut import dgutIllness


@click.command()
@click.option('-U', '--username', required=True, help="中央认证账号用户名", type=str)
@click.option('-P', '--password', required=True, help="中央认证账号密码", type=str)
@click.option('-L', '--location', help="经纬度", type=(int, float, float), multiple=True)
def main(username, password, location):
    users = username.split(",")
    pwds = password.split(",")
    locations = {item[0]: (item[1], item[2]) for item in location}
    if len(users) != len(pwds):
        exit("账号和密码个数不一致")
    for usr in enumerate(zip(users, pwds), 1):
        u = dgutIllness(usr[1][0], usr[1][1])
        if locations.get(usr[0]):
            print(u.report(locations.get(usr[0])[0], locations.get(usr[0])[1]))
        else:
            print(u.report())


if __name__ == '__main__':
    main()
