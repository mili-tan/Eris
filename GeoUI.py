from pywebio.output import put_html
from pyecharts import options as opts
from pyecharts.charts import Geo
from pyecharts.globals import ChartType, SymbolType

c = (
    Geo()
        .add_schema(maptype="world")
        .add_coordinate('Tokyo', 139.41, 35.41)
        .add(
        "",
        [("Tokyo", 55), ("上海", 66), ("杭州", 77), ("福州", 88)],
        type_=ChartType.EFFECT_SCATTER,
        color="white",
    )
        .add(
        "geo",
        [("Tokyo", "上海"), ("上海", "杭州"), ("杭州", "福州"), ("福州", "厦门")],
        type_=ChartType.LINES,
        effect_opts=opts.EffectOpts(
            symbol=SymbolType.ARROW, symbol_size=6, color="red"
        ),
        linestyle_opts=opts.LineStyleOpts(curve=0.2),
    )
        .set_series_opts(label_opts=opts.LabelOpts(is_show=False))
        .set_global_opts(title_opts=opts.TitleOpts(title="Geo-Lines"))

)

c.width = "100%"
put_html(c.render_notebook())
