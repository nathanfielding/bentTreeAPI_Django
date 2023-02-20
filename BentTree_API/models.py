from django.db import models

class Apartment(models.Model):
    id = models.AutoField(primary_key=True)
    number = models.CharField(max_length=50, unique=True, null=False)
    property = models.CharField(max_length=50, null=False)
    max_occupancy = models.IntegerField(null=False)
    occupancy = models.IntegerField(null=False)
    rented_as = models.IntegerField(null=True)

    def __str__(self):
        return self.number

class Tenant(models.Model):
    id = models.AutoField(primary_key=True)
    apartment_id = models.ForeignKey(Apartment, on_delete=models.PROTECT, null=False, blank=False)
    lease_id = models.OneToOneField('Lease', on_delete=models.CASCADE, null=False, blank=False)
    name = models.CharField(max_length=50, unique=True, null=False, blank=False)
    email = models.CharField(max_length=50, unique=True, null=False, blank=False)
    phone_number = models.CharField(max_length=50, unique=True, null=False, blank=False)
    home_address = models.CharField(max_length=50, null=False)
    is_renewing = models.BooleanField(default=False, null=True)

    def __str__(self):
        return self.name

class Lease(models.Model):
    id = models.AutoField(primary_key=True)
    tenant_id = models.OneToOneField(Tenant, on_delete=models.PROTECT, null=True, blank=False)
    apartment_id = models.ForeignKey(Apartment, on_delete=models.PROTECT, null=False, blank=False)
    start_date = models.DateField(null=False, blank=False)
    end_date = models.DateField(null=False, blank=False)
    monthly_rent = models.DecimalField(max_digits=10, decimal_places=2, null=False, blank=False)
    deposit_amount = models.DecimalField(max_digits=10, decimal_places=2, null=False, blank=False)
    copy_of_lease = models.FileField(upload_to='lease_files/', null=True)

    def __str__(self):
        # return (Tenant.objects.get(id=self.tenant_id)).name
        return str(self.id)

class MaintenanceRequest(models.Model):
    id = models.AutoField(primary_key=True)
    apartment_id = models.ForeignKey(Apartment, on_delete=models.PROTECT, null=False, blank=False)
    open_date = models.DateField(null=False, blank=False)
    close_date = models.DateField(null=True)
    description = models.CharField(max_length=100, blank=True)