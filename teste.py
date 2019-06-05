# -*- coding: utf-8 -*-

try:
    from scapy.all import *
except ImportError:
    import scapy

try:
    # This import works from the project directory
    import scapy_http.http
except ImportError:
    # If you installed this package via pip, you just need to execute this
    from scapy.layers import http
def cleanPayload(packet):
	p = str(packet)

	return p.split('Raw')[0].split("Padding")[0].replace('|','\n').strip('<')\
		.strip('bound method Ether.show of ').replace('>','').replace('[<','[')\
		.replace('\n<','<').replace('<','\n')


def full_duplex(p):
    sess = "Other"
    if 'Ether' in p:
        if 'IP' in p:
            if 'TCP' in p:
                sess = str(sorted(["TCP", p[IP].src, p[TCP].sport, p[IP].dst, p[TCP].dport],key=str))
            elif 'UDP' in p:
                sess = str(sorted(["UDP", p[IP].src, p[UDP].sport, p[IP].dst, p[UDP].dport] ,key=str))
            elif 'ICMP' in p:
                sess = str(sorted(["ICMP", p[IP].src, p[IP].dst, p[ICMP].code, p[ICMP].type, p[ICMP].id] ,key=str)) 
            else:
                sess = str(sorted(["IP", p[IP].src, p[IP].dst, p[IP].proto] ,key=str)) 
        elif 'ARP' in p:
            sess = str(sorted(["ARP", p[ARP].psrc, p[ARP].pdst],key=str)) 
        else:
            sess = p.sprintf("Ethernet type=%04xr,Ether.type%")
    return sess

def http_header(packet):
        http_packet=str(packet)
        if http_packet.find('GET'):
            print (packet.show())

def GET_print(packet):
    return "\n".join(("\n".join(packet.sprintf("{Raw:%Raw.load%}").split(r"\r\n"))




sniff(prn=GET_print, lfilter= lambda x: x.haslayer(scapy_http.http.HTTPRequest))