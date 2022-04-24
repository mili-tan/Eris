from pyecharts import options as opts
from pyecharts.charts import Line
from pywebio.output import put_html

line1 = (
    Line()
        .add_xaxis([str(x) for x in range(1, 5)])
        .add_yaxis('2015',
                   [x for x in range(1, 5)],
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
