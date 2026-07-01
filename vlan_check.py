#!/usr/bin/env python3
# Verificador de rango de VLAN

try:
    vlan = int(input("Ingrese el número de VLAN: "))
except ValueError:
    print("Error: Debe ingresar un número entero.")
    exit(1)

# Rangos según estándar: normal (1-1005) y extendido (1006-4094)
if 1 <= vlan <= 1005:
    print(f"La VLAN {vlan} pertenece al rango NORMAL.")
elif 1006 <= vlan <= 4094:
    print(f"La VLAN {vlan} pertenece al rango EXTENDIDO.")
else:
    print(f"El número {vlan} no corresponde a una VLAN válida (rango 1-4094).")
