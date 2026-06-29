import scapy.all as scapy

def process_dns_packet(packet):
    if packet.haslayer(scapy.DNSQR):
        domain = packet[scapy.DNSQR].qname.decode()

        exclude_keywords = ["fonts.", "cloud", "image", "static.", "script", "scripts", "bing", "googleads", "amazonaws", "telemetry", "googlesyndication"]
        if domain not in domains_seen and not any(keyword in domain for keyword in exclude_keywords):
            domains_seen.add(domain)
            print(f"\n[+]Dominio: {domain}")

def main():

    global domains_seen
    domains_seen = set()
    
    interface = input("\n[?] Ingrese Su interfaz de red: ")
    print(f"\n[+] Interceptando paquetes de la maquina victima...")
    scapy.sniff(iface=interface, filter="udp and port 53", prn=process_dns_packet, store=0)

if __name__ == '__main__':
    main()