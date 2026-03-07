import socket
from concurrent.futures import ThreadPoolExecutor

def scan_port(ip, port):
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(0.3)

        result = s.connect_ex((ip, port))

        s.close()

        if result == 0:
            return port

    except:
        pass

    return None


def scan_ports(ip):

    open_ports = []

    ports = range(1, 1025)

    with ThreadPoolExecutor(max_workers=100) as executor:

        results = executor.map(lambda port: scan_port(ip, port), ports)

    for port in results:
        if port:
            open_ports.append(port)

    return open_ports