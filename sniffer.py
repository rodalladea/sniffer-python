from scapy.all import sniff

def custom_action(packet):
    
    return f"Packet #{packet.summary()}"

sniff(prn=custom_action)