# urls.py
from django.urls import path
from .views import BulkOrganizationAPI, AllOrganizationsView

urlpatterns = [
    path('', AllOrganizationsView.as_view(), name='organization'),
    path('bulk/', BulkOrganizationAPI.as_view(), name='bulk_organization'),
]
