import datetime
import time

import flag
import geoip2
from pyecharts import options as opts
from pyecharts.charts import Line
from pywebio.input import *
from pywebio.output import *

import MContext
from MNetwork import MPing


def tcp():
    """TCPing | Eris"""

    clear()
    cityReader = geoip2.database.Reader('dbip-city-lite.mmdb')
    asnReader = geoip2.database.Reader('dbip-asn-lite.mmdb')

    put_html(MContext.nav)

    while True:
        target = input_group('可视化 Ping（TCP）', [
            input("目标主机：", name="ip"),
            input("目标端口：", name="port", type=NUMBER, value="80"),
            input("请求包数量：", name="pkg", type=NUMBER, value="4")
        ])
        clear("res")

        with use_scope('res'):
            with use_scope('spin'):
                put_html(MContext.spin)
                toast("正在进行Ping……")

            pings = {}
            table = [["IP", "延迟", "TTL", "状态", "位置", "ISP", "时间"]]

            for x in range(0, target["pkg"]):
                ping = MPing.Ping(target["ip"], port=target["port"]).TCP()
                pings[datetime.datetime.now().strftime("%H:%M:%S.%f")] = ping
                try:
                    r = cityReader.city(ping["ip"])
                    n = asnReader.asn(ping["ip"])
                    table.append(
                        [ping["ip"], str(ping["latency"]) + "ms", ping["ttl"],
                         ("✅" if ping["state"] is True else "❌") + ping["msg"],
                         flag.flag(str.upper(r.country.iso_code)) + " " + r.country.iso_code,
                         "AS" + str(n.autonomous_system_number) + " " + n.autonomous_system_organization,
                         datetime.datetime.now().strftime("%H:%M:%S.%f")])
                except geoip2.errors.AddressNotFoundError:
                    table.append(
                        [ping["ip"], str(ping["latency"]) + "ms", ping["ttl"],
                         ("✅" if ping["state"] is True else "❌") + " " + ping["msg"],
                         "🖥️ LAN",
                         "Local Network",
                         datetime.datetime.now().strftime("%H:%M:%S.%f")])
                time.sleep(0.5)

            toast("Ping(TCP) 完成！", color="success")
            clear("spin")

            put_table(table)

            line1 = (
                Line()
                    .add_xaxis([x for x in pings.keys()])
                    .add_yaxis(target["ip"],
                               [x["latency"] for x in pings.values()],
                               xaxis_index=0,
                               # color='#C23531',
                               color='#D770AD',
                               # is_symbol_show=False,
                               is_connect_nones=True
                               )
                    .set_global_opts(title_opts=opts.TitleOpts(title="Ping"))
            )

            put_html(line1.render_notebook())


def icmp():
    """PingICMP | Eris"""

    clear()
    cityReader = geoip2.database.Reader('dbip-city-lite.mmdb')
    asnReader = geoip2.database.Reader('dbip-asn-lite.mmdb')

    put_html(MContext.nav)

    while True:
        target = input_group('可视化 Ping（ICMP）', [
            input("目标主机：", name="ip"),
            input("请求包数量：", name="pkg", type=NUMBER, value="4")
        ])
        clear("res")

        with use_scope('res'):
            with use_scope('spin'):
                put_html(MContext.spin)
                toast("正在进行Ping……")

            pings = {}
            table = [["IP", "延迟", "TTL", "状态", "位置", "ISP", "时间"]]

            for x in range(0, target["pkg"]):
                ping = MPing.Ping(target["ip"]).ICMP()
                pings[datetime.datetime.now().strftime("%H:%M:%S.%f")] = ping
                try:
                    r = cityReader.city(ping["ip"])
                    n = asnReader.asn(ping["ip"])
                    table.append(
                        [ping["ip"], str(ping["latency"]) + "ms", ping["ttl"],
                         ("✅" if ping["state"] is True else "❌") + " " + ping["msg"],
                         flag.flag(str.upper(r.country.iso_code)) + " " + r.country.iso_code,
                         "AS" + str(n.autonomous_system_number) + " " + n.autonomous_system_organization,
                         datetime.datetime.now().strftime("%H:%M:%S.%f")])
                except geoip2.errors.AddressNotFoundError:
                    table.append(
                        [ping["ip"], str(ping["latency"]) + "ms", ping["ttl"],
                         ("✅" if ping["state"] is True else "❌") + " " + ping["msg"],
                         "🖥️ LAN",
                         "Local Network",
                         datetime.datetime.now().strftime("%H:%M:%S.%f")])
                time.sleep(0.5)

            toast("Ping(ICMP) 完成！", color="success")
            clear("spin")

            put_table(table)

            line1 = (
                Line()
                    .add_xaxis([x for x in pings.keys()])
                    .add_yaxis(target["ip"],
                               [x["latency"] for x in pings.values()],
                               xaxis_index=0,
                               # color='#C23531',
                               color='#D770AD',
                               # is_symbol_show=False,
                               is_connect_nones=True
                               )
                    # .add_yaxis('2016',
                    #            [12, 16, 20, 22, 26, 30, 35, 39, 40, 53, 68],
                    #            xaxis_index=0,
                    #            # color='#2F4554',
                    #            color='#8CC152',
                    #            is_symbol_show=False,
                    #            is_connect_nones=True)
                    .set_global_opts(title_opts=opts.TitleOpts(title="Ping"))
            )

            put_html(line1.render_notebook())
