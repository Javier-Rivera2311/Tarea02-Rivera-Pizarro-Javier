import argparse
import os
import re
import requests
import sys

oui_db_url = "http://standards-oui.ieee.org/oui/oui.txt"

def db():
    response = requests.get(oui_db_url)

    if response.status_code == 200:
        return response.text
    else:
        print("Error al descargar la base de datos de fabricantes.")
        sys.exit(1)


def mac_address(mac_address):
    mac_address = mac_address.upper()
    if re.match("^([0-9A-Fa-f]{2}[:-]){5}([0-9A-Fa-f]{2})$", mac_address):
        return mac_address.replace("-", ":")
    else:
        print("Dirección MAC inválida.")
        sys.exit(1)

def get_mac_address(mac_address, oui_db):
    mac_prefix = mac_address[:8]
    if mac_prefix in oui_db:
        return oui_db[mac_prefix]
    else:
        return "Fabricante desconocido"


def get_mac_ip(ip_address):
    response = os.popen("arp -a " + ip_address).read()
    mac_address = re.search(r"(([a-f\d]{1,2}\:){5}[a-f\d]{1,2})", response)
    if mac_address:
        return mac_address.group(0)
    else:
        return None


def get_vendor_by_ip(ip_address, oui_db):
    mac_address = get_mac_ip(ip_address)
    if mac_address:
        return get_mac_address(mac_address, oui_db)
    else:
        return None


oui_db_raw = db()


oui_db = {}
for line in oui_db_raw.splitlines():
    if "(hex)" in line:
        mac_prefix, vendor = line.split("(hex)")
        mac_prefix = mac_prefix.strip().replace("-", ":")[:8]
        vendor = vendor.strip()
        oui_db[mac_prefix] = vendor


parser = argparse.ArgumentParser(description="Herramienta para consultar el fabricante de una tarjeta de red dada su dirección MAC o su IP.")
parser.add_argument("--ip", help="IP del host a consultar.")
parser.add_argument("--mac", help="MAC a consultar. P.e. aa:bb:cc:00:00:00.")
parser.add_argument("--arp", help="Muestra los fabricantes de los host disponibles en la tabla arp.", action="store_true")
args = parser.parse_args()

if args.mac:
    mac_address = mac_address(args.mac)
    vendor = get_mac_address(mac_address, oui_db)
    print(f"MAC address: {mac_address}")
    print(f"Fabricante: {vendor}")
elif args.ip:
    if os.system(f"ping -c 1 {args.ip} > /dev/null") == 0:
        vendor = get_vendor_by_ip(args.ip, oui_db)
        if vendor:
            mac_address = get_mac_ip(args.ip)
            print(f"MAC address: {mac_address}")
            print(f"Fabricante: {vendor}")
        else:
            print("No se pudo obtener la dirección MAC.")
    else:
        print("La IP no está disponible en la red.")
elif args.arp:
    response = os.popen("arp -a").read()
    arp_table = re.findall(r"((\d{1,3}\.){3}\d{1,3})\s+([0-9A-Fa-f]{2}[:-]){5}([0-9A-Fa-f]{2})\s+(\w+)", response)
    print("IP/MAC/Vendor:")
    for arp_entry in arp_table:
        ip_address, _, mac_address, _, _ = arp_entry
        vendor = get_mac_address(mac_address, oui_db)
        print(f"{ip_address} / {mac_address} / {vendor}")
else:
    parser.print_help()