import click
from dgut_requests.dgut import dgutIllness


@click.command()
@click.option('-U', '--username', required=True, help="中央认证账号用户名", type=str)
@click.option('-P', '--password', required=True, help="中央认证账号密码", type=str)
@click.option('-L', '--location', help="经纬度")
def main(username, password, location):
    users = username.split(",")
    pwds = password.split(",")
    locations = {int(item.split(',')[0]): (float(item.split(',')[1]), float(item.split(
        ',')[2])) for item in location.strip('[]').split('],[')} if location else {}
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
