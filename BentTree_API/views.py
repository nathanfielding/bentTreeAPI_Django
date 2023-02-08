from rest_framework import generics
from django_filters.rest_framework import DjangoFilterBackend, FilterSet, DateFilter
from .serializers import *
from .models import *

class TenantList(generics.ListCreateAPIView):
    queryset = Tenant.objects.all()
    serializer_class = TenantSerializer

class TenantByName(generics.RetrieveUpdateDestroyAPIView):
    queryset = Tenant.objects.all()
    serializer_class = TenantSerializer

    #required for when returning a single object of the queryset
    lookup_field = "name"

class ApartmentNumberFilter(FilterSet):
    class Meta:
        model = Tenant
        fields = ["apartment_id__number"]
class TenantsByApartment(generics.ListAPIView):
    queryset = Tenant.objects.all()
    serializer_class = TenantSerializer
    
    # required for when returning a subset of the queryset
    filter_backends = [DjangoFilterBackend]
    filterset_class = ApartmentNumberFilter


class ApartmentList(generics.ListCreateAPIView):
    queryset = Apartment.objects.all().order_by("number")
    serializer_class = ApartmentSerializer

class ApartmentByNumber(generics.RetrieveDestroyAPIView):
    queryset = Apartment.objects.all()
    serializer_class = ApartmentSerializer

    lookup_field = "number"
