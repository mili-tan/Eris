import geoip2.database
from pyecharts import options as opts
from pyecharts.charts import Geo
from pyecharts.globals import ChartType, SymbolType
from pywebio.input import *
from pywebio.output import *
import flag

import MRoute.TCPTrace


def tcp():
    """TraceUI | Eris"""

    clear()
    cityReader = geoip2.database.Reader('dbip-city-lite.mmdb')
    asnReader = geoip2.database.Reader('dbip-asn-lite.mmdb')

    put_html("""<nav class="navbar navbar-light bg-light mb-3">
    <a class="navbar-brand" href="#">Eris</a>
    </nav>""")

    while True:

        target = input_group('可视化路由追踪（TCP）', [
            input("目标 IP：", name="ip"),
            input("目标端口：", name="port"),
        ])
        clear("res")

        with use_scope('res'):
            toast("正在进行路由追踪……")
            trace = MRoute.TCPTrace.Trace(target["ip"], int(target["port"]))
            toast("路由追踪完成！", color="success")
            table = [["IP", "位置", "", "", "ASN", "ISP"]]
            loc = []
            for x in trace["ip"]:
                try:
                    r = cityReader.city(x)
                    n = asnReader.asn(x)
                    table.append([x,
                                  flag.flag(str.upper(r.country.iso_code)) + " " + r.country.iso_code,
                                  r.subdivisions.most_specific.name if r.subdivisions.most_specific.name is not None else "",
                                  r.city.name if r.city.name is not None else "",
                                  "AS" + str(n.autonomous_system_number),
                                  n.autonomous_system_organization])

                    loc.append((",".join((r.country.iso_code,
                                          r.subdivisions.most_specific.name if r.subdivisions.most_specific.name is not None else "",
                                          r.city.name if r.city.name is not None else "")).strip(","),
                                r.location.longitude, r.location.latitude))
                except geoip2.errors.AddressNotFoundError:
                    table.append([x, "🖥️LAN", "", "", "", ""])

            loc = sorted(set(loc), key=loc.index)
            put_table(table)

            geo = Geo()
            geo.add_schema(maptype="world")

            for i in loc:
                geo.add_coordinate(i[0], i[1], i[2])
                # print(i[0], i[1], i[2])

            line = [(loc[x - 1][0], loc[x][0]) for x in range(len(loc))]
            line.pop(0)

            c = (
                geo.add(
                    "",
                    [(x[0], 1) for x in loc],
                    type_=ChartType.EFFECT_SCATTER,
                    color="red",
                )
                    .add(
                    str(target["ip"]),
                    line,
                    type_=ChartType.LINES,
                    effect_opts=opts.EffectOpts(
                        symbol=SymbolType.ARROW, symbol_size=6, color="red"
                    ),
                    linestyle_opts=opts.LineStyleOpts(curve=0.2),
                )
                    .set_series_opts(label_opts=opts.LabelOpts(is_show=False))
                    .set_global_opts(title_opts=opts.TitleOpts(title="Geo-TraceRoute"))
            )

            c.width = "100%"
            put_html(c.render_notebook())

def icmp():
    """PingUI | Eris"""

    clear()

    put_html("""<nav class="navbar navbar-light bg-light mb-3">
    <a class="navbar-brand" href="#">Eris</a>
    </nav>""")

    while True:
        target = input_group('可视化 Ping（ICMP）', [
            input("目标 IP：", name="ip"),
            input("请求包数量：", name="pkg", type=NUMBER, value="4")
        ])
        clear("res")

        with use_scope('res'):
            toast("正在进行Ping……")
            pings = {}

            for x in range(0, target["pkg"]):
                pings[datetime.datetime.now().strftime("%H:%M:%S.%f")] = MPing.ICMPing.Ping(target["ip"])

            toast("Ping(ICMP) 完成！", color="success")

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