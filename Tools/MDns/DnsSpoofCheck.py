from scapy.layers.dns import *
from scapy.layers.inet import *


def Check(domain):
    ans = sr1(IP(dst="93.184.216.34") / UDP(dport=53) /
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
