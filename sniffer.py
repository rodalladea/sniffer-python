# -*- coding: utf-8 -*-

from scapy.all import *
import requests
import json
from datetime import datetime

# Deixa o conteudo do pacote de forma ordenada e bonita
def cleanPayload(packet):
	p = str(packet)

	return p.split('Raw')[0].split("Padding")[0].replace('|','\n').strip('<')\
		.strip('bound method Ether.show of ').replace('>','').replace('[<','[')\
		.replace('\n<','<').replace('<','\n')


# Organizando para ficar no formato json
def customAction(packet):

    try:
        l2, l3, l4 = "---", "---", "---"
        srcIP, dstIP, L7protocol, size, ttl, srcMAC, dstMAC, L4protocol, srcPort, dstPort, payload = \
            "---","---","---","---","---","---","---","---","---","---","---"

        l2 = packet.summary().split("/")[0].strip();
        l3 = packet.summary().split("/")[1].strip();
        
        payload = cleanPayload(packet[0].show)

        if packet.haslayer(Ether):
            srcMAC = packet[0][0].src
            dstMAC = packet[0][0].dst
        elif packet.haslayer(Dot3):
            srcMAC = packet[0][0].src
            dstMAC = packet[0][0].dst
            if packet.haslayer(STP):
                L7protocol = 'STP'
                payload = cleanPayload(packet[STP].show)

        if packet.haslayer(Dot1Q):
            l3 = packet.summary().split("/")[2].strip()
            l4 = packet.summary().split("/")[3].strip().split(" ")[0]
        
        if packet.haslayer(ARP):
            srcMAC = packet[0][0].src
            srcIP = packet[0][0].psrc
            dstMAC = packet[0][0].dst
            dstIP = packet[0][0].pdst
            L7protocol = 'ARP'
            payload = cleanPayload(packet[0].show)
        elif (packet.haslayer(IP) or packet.haslayer(IPv6)):
            l4 = packet.summary().split("/")[2].strip().split(" ")[0]
            srcIP = packet[0][l3].src
            dstIP = packet[0][l3].dst
            
            if l3 == 'IP':
                size = packet[0][l3].len
                ttl = packet[0][l3].ttl
            elif l3 == 'IPv6':
                size = packet[0][l3].plen
                ttl = packet[0][l3].hlim

            L7protocol = packet.lastlayer().summary().split(" ")[0].strip()
            if packet.haslayer(ICMP):
                L7protocol = packet.summary().split("/")[2].strip().split(" ")[0]
                payload = packet[ICMP].summary().split("/")[0][5:]

            if packet.haslayer(TCP):
                srcPort = packet[0][l4].sport
                dstPort = packet[0][l4].dport
                L7protocol = packet.summary().split("/")[2].strip().split(" ")[0]
                L4protocol = packet.summary().split("/")[2].strip().split(" ")[0]
            elif packet.haslayer(UDP):
                srcPort = packet[0][l4].sport
                dstPort = packet[0][l4].dport
                L7protocol = packet.summary().split("/")[2].strip().split(" ")[0]
                L4protocol = packet.summary().split("/")[2].strip().split(" ")[0]
        else:
            srcMAC = "<unknown>"
            dstMAC = "<unknown>"
            l4 = "<unknown>"
            srcIP = "<unknown>"
            dstIP = "<unknown>"
            payload = cleanPayload(packet[0].show)

        jsonPacket = {"timestamp": str(datetime.now())[:-2],\
                    "srcIP": srcIP,\
                    "dstIP": dstIP,\
                    "L7protocol": L7protocol,\
                    "size": size,\
                    "ttl": ttl,\
                    "srcMAC": srcMAC,\
                    "dstMAC": dstMAC,\
                    "L4protocol": L4protocol,\
                    "srcPort": srcPort,\
                    "dstPort": dstPort,\
                    "payload": cleanPayload(packet[0].show)\
                    }

        # Define o header do protocolo
        headers = {'Content-type': 'application/json'}
        url = "http://localhost:3000"
        # Envia o jsonPacket para o destino informado
        try: 	
            r = requests.post(url, data=json.dumps(jsonPacket), headers=headers)
        except:
            print ("Não é possível realizar o post, payload vazio")
            jsonPacket["payload"] = "<unavailable>"
            r = requests.post(url, data=json.dumps(jsonPacket), headers=headers, timeout=2)
        return "Packet enviado: " + str(jsonPacket["timestamp"]) + " ; " + str(jsonPacket["srcIP"]) + " ==> " + str(jsonPacket["dstIP"] + "; " + str(jsonPacket["L4protocol"]))
    except:
        print (cleanPayload(packet[0].show))
        return "Problemas no packet, analise o problema"
    

sniff(prn=custom_action)