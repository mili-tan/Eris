import geoip2.database
from pyecharts import options as opts
from pyecharts.charts import Geo
from pyecharts.globals import ChartType, SymbolType
from pywebio.input import *
from pywebio.output import *

import MRoute.Trace

cityReader = geoip2.database.Reader('GeoLite2-City.mmdb')
asnReader = geoip2.database.Reader('GeoLite2-ASN.mmdb')

text = input("请输入目标 IP 地址：")
trace = MRoute.Trace.Trace(text)
table = [["IP", "地理位置", "", "", "ASN", "ISP"]]
loc = []
for x in trace["ip"]:
    try:
        r = cityReader.city(x)
        n = asnReader.asn(x)
        table.append([x,
                      r.country.iso_code,
                      r.subdivisions.most_specific.name if r.subdivisions.most_specific.name is not None else "",
                      r.city.name if r.city.name is not None else "",
                      "AS" + str(n.autonomous_system_number),
                      n.autonomous_system_organization])

        loc.append((",".join((r.country.iso_code,
                              r.subdivisions.most_specific.name if r.subdivisions.most_specific.name is not None else "",
                              r.city.name if r.city.name is not None else "")).strip(","),
                    r.location.longitude, r.location.latitude))
    except geoip2.errors.AddressNotFoundError:
        table.append([x, "LAN", "", "", "", ""])

loc = sorted(set(loc), key=loc.index)
put_table(table)

geo = Geo()
geo.add_schema(maptype="world")

for l in loc:
    geo.add_coordinate(l[0], l[1], l[2])
    print(l[0], l[1], l[2])

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
        str(text),
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
