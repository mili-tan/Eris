import datetime
import time

import flag
import geoip2
from pyecharts import options as opts
from pyecharts.charts import Line
from pywebio.input import *
from pywebio.output import *

from MNetwork import MPing, MDns


def mdns():
    """TCPing | Eris"""

    clear()
    cityReader = geoip2.database.Reader('dbip-city-lite.mmdb')
    asnReader = geoip2.database.Reader('dbip-asn-lite.mmdb')

    put_html(open("nav.html", "r").read())

    while True:
        target = input_group('可视化 DNS Lookup', [
            input("目标主机：", name="host")
        ])
        clear("res")

        with use_scope('res'):
            with use_scope('spin'):
                put_html(open("spin.html", "r").read())
                toast("正在进行查询……")

            table = [["状态", "响应代码", "返回数据", "返回类型"]]

            res = MDns.Dns(target["host"]).Query()

            table.append([res["state"], res["rcode"], res["rdata"], res["type"]])

            toast("查询完成！", color="success")
            clear("spin")

            put_table(table)
