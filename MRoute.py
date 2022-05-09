from scapy.layers.inet import *


class Trace:
    def __init__(self, ip, *, port=80):
        self.ip = ip
        self.port = port

    def ICMPTrace(self):
        ip = str(self.ip)

        ans, unans = sr(IP(dst=ip, ttl=(1, 30)) / ICMP(), timeout=3)
        res = {}
        for i in ans[IP]:
            if i.answer.src != ip:
                # print(i)
                res[i.answer.src] = i.query.ttl

        # res = sorted(set(res), key=res.values)
        res = sorted(res.items(), key=lambda kv: (kv[1], kv[0]))
        res = [x[0] for x in res]

        if len(res) != 0:
            return {
                "protocol": "Trace-ICMP",
                "state": True,
                "msg": "OK",
                "ip": res
            }
        else:
            return {
                "protocol": "Trace-ICMP",
                "state": False,
                "msg": "Timeout",
                "ip": res
            }

    def TCPTrace(self):
        ip = str(self.ip)
        port = int(self.port)

        ans, unans = traceroute(ip, port, maxttl=30, timeout=3)
        res = {}
        for i in ans.get_trace()[ip]:
            if ans.get_trace()[ip][i][0] != ip:
                # print(str(i) + ":" + ans.get_trace()[ip][i][0])
                res[ans.get_trace()[ip][i][0]] = i

        res = sorted(res.items(), key=lambda kv: (kv[1], kv[0]))
        res = [x[0] for x in res]

        if len(res) != 0:
            return {
                "protocol": "Trace-TCP",
                "state": True,
                "msg": "OK",
                "ip": res
            }
        else:
            return {
                "protocol": "Trace-TCP",
                "state": False,
                "msg": "Timeout",
                "ip": res
            }
