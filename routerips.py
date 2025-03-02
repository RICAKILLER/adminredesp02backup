#!/usr/bin/env python3
import re
import csv
from netmiko import ConnectHandler

# Definir los dispositivos
devices = [
    {'device_type': 'cisco_ios', 'host': ip, 'username': 'admin', 'password': 'admin'}
    for ip in ['10.0.5.5', '10.0.5.6', '10.0.5.10']
]

# Expresión regular para capturar IPs de diferentes comandos
IP_REGEX = re.compile(r'ip address (\d+\.\d+\.\d+\.\d+)')

# Función para extraer IPs desde un output de comando
def extract_ips(output):
    return {match.group(1) for match in IP_REGEX.finditer(output) if match.group(1) != "unassigned"}

# Función para conectarse a un dispositivo y obtener IPs
def get_device_ips(device):
    try:
        print(f"Conectando a {device['host']}...")
        with ConnectHandler(**device) as conn:
            output_brief = conn.send_command('show ip interface brief')
            output_config = conn.send_command('show run')
            return extract_ips(output_brief) | extract_ips(output_config)  # Unión de conjuntos
    except Exception as e:
        print(f"Error en {device['host']}: {e}")
        return set()

# Función principal
def main():
    all_router_ips = {ip for device in devices for ip in get_device_ips(device)}

    # Mostrar las IPs encontradas
    print("\nListado de IPs encontradas:")
    print("\n".join(all_router_ips))

    # Guardar en CSV
    with open('router_ips.csv', 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['IP'])
        writer.writerows([[ip] for ip in all_router_ips])

    print("\nInformación guardada en router_ips.csv")

if __name__ == "__main__":
    main()
