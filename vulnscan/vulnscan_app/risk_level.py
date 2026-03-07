import socket

def classify_risk(port):

    try:
        service = socket.getservbyport(port)

    except:
        service = "unknow"

    high_service = ["telnet","ftp","smb","betbios-ssn","microsfot-ds","rdp","ssh"]
    medium_service = ["http","https"]


    if service in high_service:
        return "High"
    
    elif service in medium_service:
        return "Medium"
    
    else:
        return "Low"