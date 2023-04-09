import scapy.all as scapy
import optparse

def scan(ip):
    # scapy.arping(ip)
    arp_request = scapy.ARP(pdst=ip)
    # print(arp_request.summary())
    # arp_request.show()
    # scapy.ls(scapy.ARP())

    broadcast = scapy.Ether(dst="ff:ff:ff:ff:ff:ff")
    # scapy.ls(scapy.Ether())
    # broadcast.show()

    arp_request_broadcast = broadcast / arp_request
    # print(arp_request_broadcast.summary())
    # arp_request_broadcast.show()
    # answered, unanswered = scapy.srp(arp_request_broadcast,timeout = 1)
    answered_list = scapy.srp(arp_request_broadcast, timeout=1, verbose=False)[0]
    # print(answered.summary())
    client_list = []

    for ele in answered_list:
        client_dict = {"ip": ele[1].psrc, "mac": ele[1].hwsrc}
        client_list.append(client_dict)
    return client_list


def print_ip_mac(result_list):
    print("IP" + "\t\t\t" + "MAC ADDRESS")
    print("-------------------------------------------------------------")
    for ele in result_list:
        print(ele["ip"] + "\t\t" + ele["mac"])

def get_ip():
    parser = optparse.OptionParser()
    parser.add_option("-t","--target",dest="ip")
    options = parser.parse_args()[0]
    ip = options.ip
    return ip

ip = get_ip()
result_list = scan(ip)
print_ip_mac(result_list)
