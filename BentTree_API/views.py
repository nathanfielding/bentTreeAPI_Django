from rest_framework import generics
from rest_framework.response import Response
from rest_framework.decorators import api_view
from .serializers import TenantSerializer, ApartmentSerializer, LeaseSerializer, MaintenanceRequestSerializer
from .models import Tenant, Apartment, Lease, MaintenanceRequest

##### START OF TENANT VIEWS ###### 
class TenantList(generics.ListCreateAPIView):
    queryset = Tenant.objects.all()
    serializer_class = TenantSerializer

@api_view(["GET", "PUT", "PATCH", "DELETE"])
def tenant_by_name(request, name):
    try:
        tenant = Tenant.objects.get(name=name)
    except:
        return Response({"error": f"No tenants with name {name} found"}, status=404)

    if request.method == "GET":
        serializer = TenantSerializer(tenant)
        return Response(serializer.data)

    elif request.method == "PUT" or request.method == "PATCH":
        serializer = TenantSerializer(tenant, data=request.data) if request.method == "PUT" else TenantSerializer(tenant, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)
    elif request.method == "DELETE":
        tenant.delete()
        return Response(status=204)

@api_view(["GET"])
def tenants_by_apartment(request, number):
    if request.method == "GET":
        tenants = Tenant.objects.filter(apartment__number=number)
        serializer = TenantSerializer(tenants, many=True)
        return Response(serializer.data)


##### START OF APARTMENT VIEWS #####
class ApartmentList(generics.ListCreateAPIView):
    queryset = Apartment.objects.all().order_by("number")
    serializer_class = ApartmentSerializer


@api_view(["GET", "PUT", "PATCH", "DELETE"])
def apartment_by_number(request, number):
    try:
        apartment = Apartment.objects.get(number=number)
    except:
        return Response({"error": f"No apartments with number {number} found"}, status=404)

    if request.method == "GET":
        serialzer = ApartmentSerializer(apartment)
        return Response(serialzer.data)
    
    elif request.method == "PUT" or request.method == "PATCH":
        serialzer = ApartmentSerializer(apartment, request.data) if request.method == "PUT" else ApartmentSerializer(apartment, request.data, partial=True)
        if serialzer.is_valid():
            serialzer.save()
            return Response(serialzer.data, status=201)
        return Response(serialzer.errors, status=400)

    elif request.method == "DELETE":
        apartment.delete()
        return Response(status=204)

@api_view(["GET"])
def available_apartments(request, end_date):
    try:
        apartments = Apartment.objects.filter(lease__end_date__lte=end_date, tenant__is_renewing=False)
    except Lease.DoesNotExist:
       return Response({"error": "No leases found"}, status=404)
   
    if request.method == "GET":
        serializer = ApartmentSerializer(apartments, many=True)
        return Response(serializer.data)

@api_view(["GET"])
def apartments_by_bedrooms(request, bedrooms):
    try:
        apartments = Apartment.objects.filter(bedrooms=bedrooms)
    except Apartment.DoesNotExist:
        return Response({"error": f"No apartments with {bedrooms} bedrooms found"}, status=404)

    if request.method == "GET":
        serializer = ApartmentSerializer(apartments, many=True)
        return Response(serializer.data, status=200)

##### START OF LEASE VIEWS #####
class LeaseList(generics.ListCreateAPIView):
    queryset = Lease.objects.all()
    serializer_class = LeaseSerializer

@api_view(["GET", "PUT", "PATCH", "DELETE"])
def lease_by_tenant_name(request, name):
    try:
        tenant = Tenant.objects.get(name=name)
    except:
        return Response({"error": f"No lease associated with {name} were found"}, status=404)
    
    lease = Lease.objects.get(tenant_id=tenant.id)
    if request.method == "GET":
        serializer = LeaseSerializer(lease)
        return Response(serializer.data, status=201)
    
    elif request.method == "PUT" or request.method == "PATCH":
        serializer = LeaseSerializer(lease, request.data) if request.method == "PUT" else LeaseSerializer(lease, request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)

    elif request.method == "DELETE":
        lease.delete()
        return Response(status=204)



##### START OF MAINTENANCE RECORD VIEWS #####
class MaintenanceRecordList(generics.ListCreateAPIView):
    queryset = MaintenanceRequest.objects.all().order_by("-open_date")
    serializer_class = MaintenanceRequestSerializer

@api_view(["GET", "PUT", "PATCH", "DELETE"])
def maintenance_request_by_apartment(request, number):
    try:
        maintenance_request = MaintenanceRequest.objects.filter(apartment__number=number)
    except Apartment.DoesNotExist:
        return Response({"error": f"No maintenance requests associated with apartment {number} were found"}, status=404)

    if request.method == "GET":
        serializer = MaintenanceRequestSerializer(maintenance_request, many=True)
        return Response(serializer.data, status=200)
    elif request.method == "PUT" or request.method == "PATCH":
        serializer = MaintenanceRequestSerializer(maintenance_request, request.data) if request.method == "PUT" else MaintenanceRequestSerializer(maintenance_request, request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)
    elif request.method == "DELETE":
        maintenance_request.delete()
        return Response(status=204)

@api_view(["GET"])
def open_maintenance_requests(request):
    try:
        maintenance_requests = MaintenanceRequest.objects.filter(close_date=None)
    except MaintenanceRequest.DoesNotExist:
        return Response({"error": "No open maintenance requests were found"}, status=404)
    
    if request.method == "GET":
        serializer = MaintenanceRequestSerializer(maintenance_requests, many=True)
        return Response(serializer.data, status=200)