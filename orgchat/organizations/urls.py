# urls.py
from django.urls import path
from .views import BulkOrganizationAPI

urlpatterns = [
    path('bulk/', BulkOrganizationAPI.as_view(), name='bulk_organization'),
]
