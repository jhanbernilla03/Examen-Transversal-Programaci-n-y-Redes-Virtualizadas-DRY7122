#!/usr/bin/env python3
"""
Script Netmiko para configurar EIGRP Nombrado en CSR1000v
y obtener información del router.
"""

from netmiko import ConnectHandler
import time

# Credenciales y conexión al router
router = {
    'device_type': 'cisco_ios',
    'host': '192.168.56.102',
    'username': 'cisco',
    'password': 'cisco123!',
    'secret': 'cisco123!',
    'port': 22,
    'timeout': 30,
    'session_timeout': 30
}

print("Conectando al router CSR1000v...")
connection = ConnectHandler(**router)
connection.enable()

print("Conexión establecida. Configurando EIGRP...")

# ============================================
# 1. HABILITAR IPv6 UNICAST ROUTING
# ============================================
connection.send_command("ipv6 unicast-routing")
time.sleep(1)

# ============================================
# 2. CONFIGURACIÓN DE EIGRP NOMBRADO (IPv4 e IPv6)
# ============================================
config_commands = [
    "router eigrp EIGRP_LAB",
    "address-family ipv4 autonomous-system 100",
    "network 192.168.56.0 0.0.0.255",
    "network 10.0.0.0 0.255.255.255",
    "eigrp router-id 1.1.1.1",
    "passive-interface default",
    "no passive-interface GigabitEthernet1",
    "exit-address-family",
    "address-family ipv6 autonomous-system 100",
    "network 3001:ABCD:ABCD::/64",
    "eigrp router-id 1.1.1.1",
    "passive-interface default",
    "no passive-interface GigabitEthernet1",
    "exit-address-family",
]

output_config = connection.send_config_set(config_commands)
print("Configuración EIGRP enviada:")
print(output_config)

time.sleep(2)

# ============================================
# 3. SHOW RUNNING-CONFIG | SECTION EIGRP
# ============================================
print("\n" + "="*60)
print("SHOW RUNNING-CONFIG | SECTION EIGRP")
print("="*60)
output_eigrp = connection.send_command("show running-config | section eigrp")
print(output_eigrp)

# ============================================
# 4. SHOW IP INTERFACE BRIEF
# ============================================
print("\n" + "="*60)
print("SHOW IP INTERFACE BRIEF")
print("="*60)
output_interfaces = connection.send_command("show ip interface brief")
print(output_interfaces)

# ============================================
# 5. SHOW RUNNING-CONFIG COMPLETO
# ============================================
print("\n" + "="*60)
print("OBTENIENDO RUNNING-CONFIG COMPLETO...")
print("="*60)
output_running = connection.send_command("show running-config")
print("Guardando en archivo...")
with open("running_config_router.txt", "w") as f:
    f.write(output_running)
print("Archivo 'running_config_router.txt' creado.")

# ============================================
# 6. SHOW VERSION
# ============================================
print("\n" + "="*60)
print("SHOW VERSION")
print("="*60)
output_version = connection.send_command("show version")
print(output_version)
with open("show_version_router.txt", "w") as f:
    f.write(output_version)
print("Archivo 'show_version_router.txt' creado.")

# ============================================
# GUARDAR CONFIGURACIÓN
# ============================================
connection.send_command("write memory")
print("\nConfiguración guardada en memoria.")

connection.disconnect()
print("Conexión cerrada. Script finalizado.")
