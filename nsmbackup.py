import os
import datetime
from netmiko import ConnectHandler

# Configuración de los dispositivos
devices = [
    {'device_type': 'cisco_ios', 'host': ip, 'username': 'admin', 'password': 'admin'}
    for ip, name in zip(['10.0.5.5', '10.0.5.6', '10.0.5.10'], ['router1', 'router2', 'router3'])
]

# Carpeta base para almacenar los backups
BACKUP_DIR = "backups"
os.makedirs(BACKUP_DIR, exist_ok=True)

# Función para extraer la configuración de un dispositivo
def backup_config(device):
    try:
        print(f"Conectando a {device['host']}...")
        with ConnectHandler(**device) as conn:
            output = conn.send_command('show running-config')
            
            # Crear carpeta por dispositivo
            device_dir = os.path.join(BACKUP_DIR, device['host'])
            os.makedirs(device_dir, exist_ok=True)
            
            # Definir el nombre del archivo de backup con fecha y hora
            timestamp = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
            backup_file = os.path.join(device_dir, f"backup_{timestamp}.txt")
            
            # Guardar el backup en el archivo
            with open(backup_file, 'w') as f:
                f.write(output)
            
            # Crear archivo backup_time_date.txt
            backup_time_file = os.path.join(device_dir, "backup_time_date.txt")
            with open(backup_time_file, 'w') as f:
                f.write(f"Backup realizado el: {timestamp}\n")
                f.write(f"Configuración del router {device['host']} guardada correctamente.\n")
            
            print(f"Backup de {device['host']} realizado correctamente.")
            return backup_file
    except Exception as e:
        print(f"Error en {device['host']}: {e}")
        return None

# Función principal
def main():
    for device in devices:
        print("\n--- Ejecutando backup ---")
        backup_file = backup_config(device)
        if backup_file:
            print(f"Backup guardado en: {backup_file}")
        else:
            print(f"No se pudo realizar el backup para {device['host']}.")
        
    print("\nTodos los backups se han completado.")

if __name__ == "__main__":
    main()
