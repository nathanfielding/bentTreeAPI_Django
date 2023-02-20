from rest_framework import generics
from rest_framework.response import Response
from rest_framework.decorators import api_view
from .serializers import TenantSerializer, ApartmentSerializer, LeaseSerializer
from .models import Tenant, Apartment, Lease

##### START OF TENANT VIEWS #####

# @api_view(["GET", "POST"])
# def tenant_list(request):
#     if request.method == "GET":
#         tenants = Tenant.objects.all()
#         serializer = TenantSerializer(tenants, many=True)
#         return Response(serializer.data)
    
#     elif request.method == "POST":
#         serializer = TenantSerializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data, status=201)
#         return Response(serializer.errors, status=400)

class TenantList(generics.ListCreateAPIView):
    queryset = Tenant.objects.all()
    serializer_class = TenantSerializer


@api_view(["GET", "PUT", "PATCH", "DELETE"])
def tenant_by_name(request, name):
    try:
        tenant = Tenant.objects.get(name=name)
    except:
        return Response(status=404)

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

# class TenantByName(generics.RetrieveUpdateDestroyAPIView):
#     queryset = Tenant.objects.all()
#     serializer_class = TenantSerializer

#     #required for when returning a single object of the queryset
#     lookup_field = "name"

@api_view(["GET"])
def tenants_by_aparment(request, number):
    try:
        apartment = Apartment.objects.get(number=number)
    except:
        return Response(status=404)

    if request.method == "GET":
        tenants = Tenant.objects.filter(apartment_id=apartment.id)
        serializer = TenantSerializer(tenants, many=True)
        return Response(serializer.data)

# class TenantsByApartment(generics.ListAPIView):
#     queryset = Tenant.objects.all()
#     serializer_class = TenantSerializer

##### START OF APARTMENT VIEWS #####

# @api_view(["GET", "POST"])
# def apartment_list(request):
#     if request.method == "GET":
#         apartments = Apartment.objects.all()
#         serializer = ApartmentSerializer(apartments, many=True)
#         return Response(serializer.data)

#     elif request.method == "POST":
#         serializer = ApartmentSerializer(request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data, status=201)
#         return Response(serializer.errors, status=400)

class ApartmentList(generics.ListCreateAPIView):
    queryset = Apartment.objects.all().order_by("number")
    serializer_class = ApartmentSerializer


@api_view(["GET", "PUT", "PATCH", "DELETE"])
def apartment_by_number(request, number):
    try:
        apartment = Apartment.objects.get(number=number)
    except:
        return Response(status=404)

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

# class ApartmentByNumber(generics.RetrieveDestroyAPIView):
#     queryset = Apartment.objects.all()
#     serializer_class = ApartmentSerializer

#     lookup_field = "number"

@api_view(["GET"])
def apartments_by_end_date(request, end_date):
    try:
        leases = Lease.objects.get(end_date<=end_date)
    except:
       return Response(status=404)
   
    if request.method == "GET":
        apartments = []
        for lease in leases:
            apartments.append(Apartment.objects.get(id=lease.apartment_id))
        serializer = ApartmentSerializer(apartments, many=True)
        return Response(serializer.data)


##### START OF LEASE VIEWS #####

@api_view(["GET", "POST"])
def lease_list(request):
    if request.method == "GET":
        leases = Lease.objects.all()
        serializer = LeaseSerializer(leases, many=True)
        return Response(serializer.data)

    elif request.method == "POST":
        serializer = LeaseSerializer(request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)

class LeaseList(generics.ListCreateAPIView):
    queryset = Lease.objects.all()
    serializer_class = LeaseSerializer

@api_view(["GET", "PUT", "PATCH", "DELETE"])
def lease_by_tenant(request, name):
    try:
        tenant = Tenant.objects.get(name=name)
    except:
        return Response(status=404)
    
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