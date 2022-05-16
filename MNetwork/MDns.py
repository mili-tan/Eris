from scapy.layers.dns import *
from scapy.layers.inet import *


class Dns:
    def __init__(self, domain):
        self.domain = domain

    def Query(self, server="8.8.8.8", port=53):
        domain = self.domain

        ans = sr1(IP(dst=server) / UDP(dport=port) /
                  DNS(rd=1, qd=DNSQR(qname=domain)))
        if len(ans) != 0:
            if ans[DNS].rcode != 0:
                return {
                    "protocol": "dns",
                    "state": False,
                    "msg": "DNS Error",
                    "rcode": str(ans[DNS].rcode),
                    "rdata": "",
                    "type": ""
                }

            for x in range(ans[DNS].ancount):
                if ans[DNSRR][x].type == 1:
                    return {
                        "protocol": "dns",
                        "state": True,
                        "msg": "OK",
                        "rcode": str(ans[DNS].rcode),
                        "rdata": str(ans[DNSRR][0].rdata),
                        "type": str(ans[DNSRR][0].type)
                    }

            return {
                "protocol": "dns",
                "state": True,
                "msg": "OK",
                "rcode": str(ans[DNS].rcode),
                "rdata": str(ans[DNSRR][0].rdata),
                "type": str(ans[DNSRR][0].type)
            }
        else:
            return {
                "protocol": "dns",
                "state": False,
                "msg": "Timeout"
            }

    def SpoofCheck(self, server="93.184.216.34", port=53):
        domain = self.domain

        ans = sr1(IP(dst=server) / UDP(dport=port) /
                  DNS(rd=1, qd=DNSQR(qname=domain)), timeout=2)
        if ans is not None and len(ans) != 0 and ans[DNS].rcode == 0:
            return {
                "protocol": "dns",
                "state": True,
                "spoof": True,
                "msg": "probably",
                "rcode": str(ans[DNS].rcode),
                "rdata": str(ans[DNSRR][0].rdata),
                "type": str(ans[DNSRR][0].type)
            }
        else:
            return {
                "protocol": "dns",
                "state": True,
                "spoof": False,
                "msg": "probably not"
            }
