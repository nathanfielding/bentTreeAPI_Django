from django.db import models

class Tenant(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50, unique=True, null=False)
    email = models.CharField(max_length=50, unique=True, null=False)
    phone_number = models.CharField(max_length=50, unique=True, null=False)
    home_address = models.CharField(max_length=50, null=False)
    is_renewing = models.BooleanField(default=False, null=True)

    def __str__(self):
        return self.name

class Apartment(models.Model):
    id = models.AutoField(primary_key=True)
    number = models.CharField(max_length=50, unique=True, null=False)
    occupancy = models.IntegerField(null=False)

    def __str__(self):
        return self.number

class Lease(models.Model):
    id = models.AutoField(primary_key=True)
    tenant_id = models.ForeignKey(Tenant, on_delete=models.PROTECT, null=False)
    aparment_id = models.ForeignKey(Apartment, on_delete=models.PROTECT, null=False)
    start_date = models.DateField(null=False)
    end_date = models.DateField(null=False)
    monthly_rent = models.DecimalField(max_digits=10, decimal_places=2, null=False)
    deposit_amount = models.DecimalField(max_digits=10, decimal_places=2, null=False)
    copy_of_lease = models.FileField(upload_to='lease_files/', null=False)

class MaintenanceRequest(models.Model):
    id = models.AutoField(primary_key=True)
    apartment_id = models.ForeignKey(Apartment, on_delete=models.PROTECT, null=False)
    open_date = models.DateField(null=False)
    close_date = models.DateField(null=True)
    description = models.CharField(max_length=100, blank=True)