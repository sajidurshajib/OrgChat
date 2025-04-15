from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from rest_framework import status
from .models import Organization
from .serializers import OrganizationSerializer, OrganizationSerializerWithId, OrganizationDeleteSerializer
from utils.superuser import IsSuperUser
from rest_framework.generics import ListAPIView

from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi


class AllOrganizationsPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 100

class AllOrganizationsView(APIView):
    permission_classes = [IsAuthenticated]  

    def get(self, request):
        queryset = Organization.objects.all().order_by("id")
        paginator = AllOrganizationsPagination()
        page = paginator.paginate_queryset(queryset, request)
        serializer = OrganizationSerializerWithId(page, many=True)
        return paginator.get_paginated_response(serializer.data)


class BulkOrganizationAPI(APIView):
    permission_classes = [IsSuperUser]

    @swagger_auto_schema(
        request_body=OrganizationSerializer(many=True),
        responses={201: OrganizationSerializer(many=True)}
    )
    def post(self, request):
        serializer = OrganizationSerializer(data=request.data, many=True)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "Created successfully", "data": serializer.data}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


    @swagger_auto_schema(
        request_body=OrganizationSerializer(many=True),
        responses={201: OrganizationSerializer(many=True)}
    )
    def put(self, request):
        updated_items = []
        errors = []

        for item in request.data:
            try:
                obj = Organization.objects.get(id=item['id'])
                serializer = OrganizationSerializer(obj, data=item, partial=True)
                if serializer.is_valid():
                    serializer.save()
                    updated_items.append(serializer.data)
                else:
                    errors.append(serializer.errors)
            except Organization.DoesNotExist:
                errors.append({'id': item.get('id'), 'error': 'Not found'})

        return Response({"updated": updated_items, "errors": errors})


    @swagger_auto_schema(
        request_body=OrganizationDeleteSerializer,
        responses={200: 'Successfully deleted'}
    )
    def delete(self, request):
        ids = request.data.get("ids", [])
        deleted_count, _ = Organization.objects.filter(id__in=ids).delete()
        return Response({"message": f"{deleted_count} items deleted"}, status=status.HTTP_200_OK)
