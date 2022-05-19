from scapy.layers.inet import *

from MNetwork import MHost


class Trace:
    def __init__(self, ip, *, port=80):
        self.ip = MHost.Host(str(ip)).GetHost()
        self.port = port

    def ICMP(self):
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
            return __getJson__("Trace-ICMP", True, "OK", res)
        else:
            return __getJson__("Trace-ICMP", False, "Timeout", res)

    def TCP(self):
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
            return __getJson__("Trace-TCP", True, "OK", res)
        else:
            return __getJson__("Trace-TCP", False, "Timeout", res)


def __getJson__(protocol, state, msg, res):
    return {
        "protocol": protocol,
        "state": state,
        "msg": msg,
        "ip": res
    }
