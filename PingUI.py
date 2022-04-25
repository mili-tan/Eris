import datetime
import time

from pyecharts import options as opts
from pyecharts.charts import Line
from pywebio.input import *
from pywebio.output import *
import MPing.TCPing

import MPing.ICMPing


def index():
    """PingUI | Eris"""

    clear()

    put_html("""<nav class="navbar navbar-light bg-light mb-3">
    <a class="navbar-brand" href="#">Eris</a>
    </nav>""")

    while True:
        target = input_group('可视化 Ping（TCP）', [
            input("目标 IP：", name="ip"),
            input("目标端口：", name="port", type=NUMBER, value="80"),
            input("请求包数量：", name="pkg", type=NUMBER, value="4")
        ])
        clear("res")

        with use_scope('res'):
            toast("正在进行Ping……")
            pings = {}

            for x in range(0, target["pkg"]):
                pings[datetime.datetime.now().strftime("%H:%M:%S.%f")] = MPing.TCPing.Ping(target["ip"], target["port"])
                time.sleep(0.5)

            toast("Ping(TCP) 完成！", color="success")

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
