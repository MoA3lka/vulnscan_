from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login
from .models import Device, ScanResults, Alert
from .port_scan import scan_ports
from .risk_level import classify_risk
import socket
import ipaddress

    
#login page
def login_view(request):

    if request.method == "POST":

        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect("dashboard")
        

    return render(request, "login.html")

# Dashboard Page
@login_required
def dashboard(request):

    # Statistics
    total_devices = Device.objects.count()
    total_ports = ScanResults.objects.count()
    total_alerts = Alert.objects.filter(severity="High").count()

    # Recent Results
    results = ScanResults.objects.order_by('-timestamp')[:5]

    # Recent alerts
    alerts = Alert.objects.filter(severity="High")[:5]

    context ={
        "total_devices": total_devices,
        "total_ports": total_ports,
        "total_alerts": total_alerts,
        "results": results,
        "alerts": alerts

    }

    return render(request,"dashboard.html",context)

# validate ip/ hostname
def validate_target(target):
    try:
        ipaddress.ip_address(target)
        return True
    except ValueError:
        return False
    
@login_required
def start_scan(request):

    if request.method == "POST":

        ip = request.POST.get("ip_address", "").strip()

        print("IP received:", ip)

        if not ip:
            return render(request, "start_scan.html", {
                "error": "Please enter an IP address"
            })

        if not validate_target(ip):
            return render(request, "start_scan.html", {
                "error": "Enter a valid IP address"
            })

        device = Device.objects.create(ip_address=ip)

        ports = scan_ports(ip)

        for port in ports:
            risk = classify_risk(port)

            result = ScanResults.objects.create(
                device=device,
                port=port,
                risk_level=risk
            )

        return redirect("Scan_Result")

    return render(request, "start_scan.html")
        
# Scan Results Page

@login_required
def results(request):

    latest_device = Device.objects.order_by('-last_scan').first()

    latest_results = None

    if latest_device:
        latest_results = ScanResults.objects.filter(device=latest_device)


    devices = Device.objects.all().order_by('-last_scan')
    all_results = ScanResults.objects.all().order_by('-timestamp')

    context = {
        "latest_device": latest_device,
        "latest_results": latest_results,
        "devices": devices,
        "all_results": all_results

    }

    return render(request, "Scan_Result.html", context)

# Alert Page
@login_required
def alerts(request):

    alerts = Alert.objects.filter(severity="High").order_by('-id')

    context = {"alerts": alerts}
    return render(request, "alerts.html",{
        "alerts": alerts
    })