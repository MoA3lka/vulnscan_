from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Device, ScanResults, Alert
from .port_scan import scan_ports
from .risk_level import classify_risk

# Dashboard Page
@login_required
def dashboard(request):

    # Statistics
    total_devices = Device.objects.count()
    total_ports = ScanResults.objects.count()
    total_alerts = Alert.objects.filter(severity="High").count

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


# Start Scan Page
@login_required
def start_scan(request):

    if request.method =="POST":

        ip = request.POST.get("ip")

        # Save Device
        device = Device.objects.create(ip_address=ip)

        # Run Scanner
        ports = scan_ports(ip)

        for port in ports:

            risk = classify_risk(port)

            # Save scan result
            result = ScanResults.objects.create(
                device=device,
                port=port,
                risk_level=risk
            )

            # Create alert if high risk
            if risk == "High":
                Alert.objects.create(
                    result=result,
                    severity="High"
                )

                return redirect("results")
            
            return render(request, "start_scan.html")
        
# Scan Results Page

@login_required
def results(request):

    results = ScanResults.objects.all().order_by('-timestamp')

    return render(request, "scan_results.html", {
        "results": results
    })

# Alert Page
@login_required
def alerts(request):

    alerts = Alert.objects.filter(severity="High").order_by('-id')

    return render(request, "alerts.html",{
        "alerts": alerts
    })