import geoip2.database
from pyecharts import options as opts
from pyecharts.charts import Geo
from pyecharts.globals import ChartType, SymbolType
from pywebio.input import *
from pywebio.output import *
import flag

import MGeoData
import MContext
from MNetwork import MRoute

cityReader = MGeoData.cityReader
asnReader = MGeoData.asnReader


def tcp():
    """TraceUI | Eris"""

    clear()
    put_html(MContext.nav)

    while True:

        target = input_group('可视化路由追踪（TCP）', [
            input("目标主机：", name="ip"),
            input("目标端口：", name="port", type=NUMBER, value="80"),
        ])
        clear("res")

        with use_scope('res'):
            toast("正在进行路由追踪……")
            with use_scope('spin'):
                put_html(MContext.spin)
            trace = MRoute.Trace(target["ip"], port=int(target["port"])).ICMP()
            toast("路由追踪完成！", color="success")
            clear("spin")
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
    """TraceUI | Eris"""

    clear()

    put_html(MContext.nav)

    while True:

        target = input_group('可视化路由追踪（ICMP）', [
            input("目标主机：", name="ip")
        ])
        clear("res")

        with use_scope('res'):
            toast("正在进行路由追踪……")
            with use_scope('spin'):
                put_html(MContext.spin)
            trace = MRoute.Trace(target["ip"]).TCP()
            toast("路由追踪完成！", color="success")
            clear("spin")
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
