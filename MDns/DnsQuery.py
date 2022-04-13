from scapy.layers.dns import *
from scapy.layers.inet import *

def Query(domain):
    ans = sr1(IP(dst="8.8.8.8") / UDP(dport=53) /
                   DNS(rd=1, qd=DNSQR(qname=domain)))
    if len(ans) != 0:
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