from rest_framework import generics
from django_filters.rest_framework import DjangoFilterBackend, FilterSet, DateFilter
from .serializers import *
from .models import *

class TenantList(generics.ListCreateAPIView):
    queryset = Tenant.objects.all()
    serializer_class = TenantSerializer
