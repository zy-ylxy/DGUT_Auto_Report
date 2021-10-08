from gevent import monkey;monkey.patch_all()
import click
from dgut_requests.dgut import dgutIllness
from retry import retry
import gevent


@retry(tries=50, delay=2, backoff=2, max_delay=30)
def clock(u: dgutIllness, location: "list | None" = None) -> None:
    '''
    打卡并输出结果
    :param u: dgutIllness, 指定打卡的dgutIllness对象.
    :param location: list | None, 指定打卡的定位（经纬度列表类型）或缺省None.
    :returns: None，打印结果
    '''
    if location:
        print(u.username[-2:], '-', u.report(location[0], location[1]))
    else:
        print(u.username[-2:], '-', u.report())


@click.command()
@click.option('-U', '--username', required=True, help="中央认证账号用户名", type=str)
@click.option('-P', '--password', required=True, help="中央认证账号密码", type=str)
@click.option('-L', '--location', help="经纬度")
def main(username, password, location):
    users = username.split(",")
    pwds = password.split(",")
    locations = {int(item.split(',')[0]): (float(item.split(',')[1]), float(item.split(
        ',')[2])) for item in location.strip('[] ').split('],[')} if location else {}
    if len(users) != len(pwds):
        exit("账号和密码个数不一致")
    tasks = []
    for usr in enumerate(zip(users, pwds), 1):
        u = dgutIllness(usr[1][0], usr[1][1])
        tasks.append(gevent.spawn(clock, u=u, location=locations.get(usr[0])))
    gevent.joinall(tasks)

if __name__ == '__main__':
    main()
