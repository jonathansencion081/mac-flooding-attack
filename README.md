# MAC Flooding Attack Script
**Autor:** Jonathan Sención  
**Matrícula:** 20250851  
**Institución:** ITLA - Instituto Tecnológico de las Américas  

---

## Objetivo del Laboratorio
Demostrar cómo un atacante puede saturar la tabla CAM (Content Addressable Memory) 
de un switch Cisco enviando miles de tramas con MACs falsas y aleatorias, forzando 
al switch a comportarse como un hub y enviando tráfico a todos los puertos.

---

## Objetivo del Script
Generar tramas Ethernet masivas con MACs e IPs de origen aleatorias para llenar 
completamente la tabla MAC del switch víctima, causando que reenvíe todo el tráfico 
en broadcast y permitiendo al atacante interceptar comunicaciones.

### Parámetros Usados
| Parámetro | Valor | Descripción |
|---|---|---|
| `src` | `RandMAC()` | MAC origen aleatoria |
| `dst` | `RandMAC()` | MAC destino aleatoria |
| `src IP` | `RandIP()` | IP origen aleatoria |
| `dst IP` | `RandIP()` | IP destino aleatoria |
| `iface` | `eth0` | Interfaz de red atacante |

### Requisitos
- Kali Linux
- Python 3
- Scapy (`sudo apt install python3-scapy`)
- Ejecutar como root (`sudo`)

---

## Funcionamiento del Script
1. Se generan MACs e IPs completamente aleatorias por cada trama
2. Las tramas se envían continuamente al switch
3. El switch aprende cada MAC falsa y la agrega a su tabla CAM
4. La tabla CAM se llena hasta su capacidad máxima
5. El switch entra en modo fail-open y reenvía tráfico a todos los puertos
6. El atacante puede capturar tráfico de otros hosts con Wireshark

---

## Topología de Red
[Kali Atacante] eth0 ──── e0/2 [SW1] e0/0 ──── e0/0 [SW2] e0/1 ──── eth0 [VPC1]
192.168.85.10                10.20.25.1              10.20.25.2         192.168.85.20
│
e0/1 └──── e0/0 [SW3] e0/1 ──── eth0 [VPC2]
10.20.25.3         192.168.51.20

### VLANs
| VLAN | Nombre | Red |
|---|---|---|
| VLAN 10 | VLAN10-20250851 | 192.168.85.0/24 |
| VLAN 20 | VLAN20-20250851 | 192.168.51.0/24 |
| Management | MGMT | 10.20.25.0/24 |

---

## Ejecución
```bash
sudo python3 mac_flooding.py
```

### Verificación del Ataque
En SW1:
show mac address-table count
show mac address-table dynamic
Se observarán miles de entradas MAC falsas en la tabla CAM.

---

## Capturas de Pantalla
<img width="641" height="599" alt="image" src="https://github.com/user-attachments/assets/d9f66b28-0042-4225-bb05-4c33a793fceb" />

<img width="762" height="312" alt="image" src="https://github.com/user-attachments/assets/7f020ee5-70cb-4fb1-9a74-15036ee322f5" />

<img width="632" height="663" alt="image" src="https://github.com/user-attachments/assets/cb656d37-1163-4059-b612-b9ebb6155cea" />

---

## Contramedidas
### 1. Port Security — Limitar MACs por puerto
interface e0/2
switchport mode access
switchport port-security
switchport port-security maximum 2
switchport port-security violation shutdown
switchport port-security mac-address sticky
### 2. Verificación de Port Security
show port-security
show port-security interface e0/2
show port-security address
### 3. Reducir el tiempo de aging de la tabla MAC
mac address-table aging-time 30
### 4. 802.1X autenticación de puerto
Implementar autenticación por puerto para que solo dispositivos 
autorizados puedan conectarse a la red.
