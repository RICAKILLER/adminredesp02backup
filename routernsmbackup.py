import os
import re
import datetime
import hashlib
import subprocess
from netmiko import ConnectHandler

# Configuración de los dispositivos
devices = [
    {'device_type': 'cisco_ios', 'host': ip, 'username': 'admin', 'password': 'admin'}
    for ip in ['10.0.5.5', '10.0.5.6', '10.0.5.10']
]
<<<<<<< HEAD
=======
# Diccionario de nombres personalizados para cada router
ROUTER_NAMES = {
    '10.0.5.5': 'Router1',
    '10.0.5.6': 'Router2',
    '10.0.5.10': 'Router3'
}

>>>>>>> 7bd6080 (Primer commit - Configuración inicial de backups)

# Carpeta base para almacenar los backups
BACKUP_DIR = "backups"
os.makedirs(BACKUP_DIR, exist_ok=True)

# Función para obtener el hash de un archivo
def file_hash(filename):
    if not os.path.exists(filename):
        return None
    with open(filename, 'rb') as f:
        return hashlib.md5(f.read()).hexdigest()

# Función para extraer la configuración de un dispositivo
def backup_config(device):
    try:
        print(f"Conectando a {device['host']}...")
        with ConnectHandler(**device) as conn:
            output = conn.send_command('show running-config')
            
            # Crear carpeta por dispositivo
<<<<<<< HEAD
            device_dir = os.path.join(BACKUP_DIR, device['host'])
=======
            # Crear carpeta por dispositivo con el nombre personalizado
            device_name = ROUTER_NAMES.get(device['host'], device['host'])  # Usa el nombre si existe, sino, la IP
            device_dir = os.path.join(BACKUP_DIR, device_name)
>>>>>>> 7bd6080 (Primer commit - Configuración inicial de backups)
            os.makedirs(device_dir, exist_ok=True)
            
            # Definir el nombre del archivo
            timestamp = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
            new_backup_file = os.path.join(device_dir, f"backup_{timestamp}.txt")
            latest_backup_file = os.path.join(device_dir, "latest_backup.txt")
            
            # Guardar nuevo backup
            with open(new_backup_file, 'w') as f:
                f.write(output)
            
            # Comparar con el último backup
            if file_hash(new_backup_file) != file_hash(latest_backup_file):
                print(f"Cambios detectados en {device['host']}, actualizando backup...")
                os.replace(new_backup_file, latest_backup_file)
                return latest_backup_file
            else:
                print(f"No hay cambios en {device['host']}, se mantiene el backup previo.")
                os.remove(new_backup_file)
                return None
    except Exception as e:
        print(f"Error en {device['host']}: {e}")
        return None

# Función para subir cambios a GitHub
def upload_to_github():
    try:
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        subprocess.run(["git", "add", "backups/"], check=True)
        subprocess.run(["git", "commit", "-m", f"Backup actualizado {timestamp}"], check=True)
        subprocess.run(["git", "branch", "-M", "main"], check=True)
<<<<<<< HEAD
        subprocess.run(["git", "remote", "add", "origin", "https://github.com/RICAKILLER/adminredesp02backup.git"], check=True)
=======
>>>>>>> 7bd6080 (Primer commit - Configuración inicial de backups)
        subprocess.run(["git", "push", "-u", "origin", "main"], check=True)
        print("Backups subidos a GitHub correctamente.")
    except subprocess.CalledProcessError as e:
        print(f"Error al subir a GitHub: {e}")

# Función principal
def main():
    updated_files = [backup_config(device) for device in devices]
    if any(updated_files):
        upload_to_github()
    else:
        print("No hubo cambios en ningún router. No se subieron archivos a GitHub.")

if __name__ == "__main__":
    main()
