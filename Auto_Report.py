import click
from dgut_requests.dgut import dgutIllness


@click.command()
@click.option('-U', '--username', required=True, help="中央认证账号用户名", type=str)
@click.option('-P', '--password', required=True, help="中央认证账号密码", type=str)
@click.option('-L', '--location', help="经纬度", nargs=2, type=float, default=(113.87651, 22.90701))
def main(username, password, location):
    users = username.split(",")
    pwds = password.split(",")
    if len(users) != len(pwds):
        exit("账号和密码个数不一致")
    for usr in zip(users, pwds):
        u = dgutIllness(usr[0], usr[1])
        print(u.report(location[0], location[1]))


if __name__ == '__main__':
    main()
