"""BentTree_WebApp URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from BentTree_API import views

urlpatterns = [
    path('admin/', admin.site.urls),

    # tenant endpoints
    path("tenants/", views.TenantList.as_view()),
    path("tenants/by-name/<str:name>/", views.tenant_by_name),
    path("tenants/by-apartment/<str:number>/", views.tenants_by_apartment),

    # apartment endpoints
    path("apartments/", views.ApartmentList.as_view()),
    path("apartments/by-number/<str:number>/", views.apartment_by_number),
    path("apartments/by-availability_date/<str:end_date>/", views.available_apartments),
    path("apartments/by-bedrooms/<int:bedrooms>/", views.apartments_by_bedrooms),

    # lease endpoints
    path("leases/", views.LeaseList.as_view()),
    path("leases/by-name/<str:name>", views.lease_by_tenant_name),

    # path("leases/<int:id>", views.LeasebyId.as_view())
]
