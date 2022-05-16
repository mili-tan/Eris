import flag
import geoip2
from pywebio.input import *
from pywebio.output import *

from MNetwork import MDns, MHost


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

            table = [["状态", "响应代码", "返回数据", "返回类型", "地理位置", "ISP"]]

            res = MDns.Dns(target["host"]).Query()

            if MHost.Host(res["rdata"]).isIp():
                r = cityReader.city(res["rdata"])
                n = asnReader.asn(res["rdata"])
                loc = flag.flag(str.upper(r.country.iso_code)) + " " + r.country.iso_code + \
                      r.subdivisions.most_specific.name if r.subdivisions.most_specific.name is not None else "" + \
                      r.city.name if r.city.name is not None else ""
                isp = "AS" + str(n.autonomous_system_number) + " " + n.autonomous_system_organization
                table.append([res["state"], res["rcode"], res["rdata"], res["type"], loc, isp])
            else:
                table.append([res["state"], res["rcode"], res["rdata"], res["type"], "", ""])

            toast("查询完成！", color="success")
            clear("spin")

            put_table(table)
