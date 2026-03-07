import socket

def scan_ports(ip):

    open_ports = []

    for port in range(1,1025):

        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(0.5)

        result = s.connect_ex((ip,port))

        if result == 0:
            open_ports.append(port)

        
        s.close()

    
    return open_ports
