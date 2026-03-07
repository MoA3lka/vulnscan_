from django.db import models

class Device(models.Model):

    ip_address = models.CharField(max_length=50)
    hostname = models.CharField(max_length=100, blank=True, null=True)
    last_scan = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.ip_address
    

class ScanResults(models.Model):

    device = models.ForeignKey(Device, on_delete=models.CASCADE)
    port = models.IntegerField()
    risk_level = models.CharField(max_length=20)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.device.ip_address}:{self.port}"

class Alert(models.Model):

    result = models.ForeignKey(ScanResults, on_delete=models.CASCADE)
    severity = models.CharField(max_length=20)
    status = models.CharField(max_length=20, default="Open")

    def __str__(self):
        return self.severity

