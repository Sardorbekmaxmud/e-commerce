from rest_framework.views import APIView
from rest_framework import status, permissions
from rest_framework.response import Response
from drf_yasg.utils import swagger_auto_schema

from products.models import ProductViewHistory
from products.serializers import ProductViewHistorySerializer
from products.views import CustomPagination
from products.permissions import IsStaffOrReadOnly


class ProductViewHistoryListCreate(APIView):
    serializer_class = ProductViewHistorySerializer
    pagination_class = CustomPagination
    permission_classes = [permissions.IsAuthenticated, IsStaffOrReadOnly]

    @swagger_auto_schema(method='get')
    def get(self, request):
        queryset = ProductViewHistory.objects.all()

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_paginated_response(self.serializer_class(page, many=True).data)
        else:
            serializer = self.serializer_class(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @swagger_auto_schema(request_body=ProductViewHistorySerializer)
    def post(self, request):
        serializer = ProductViewHistorySerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @property
    def paginator(self):
        if not hasattr(self, '_paginator'):
            if self.pagination_class is None:
                self._paginator = None
            else:
                self._paginator = self.pagination_class()
        else:
            pass
        return self._paginator

    def paginate_queryset(self, queryset):
        if self.paginator is None:
            return None
        return self.paginator.paginate_queryset(queryset,
                                                self.request, view=self)

    def get_paginated_response(self, data):
        assert self.paginator is not None
        return self.paginator.get_paginated_response(data)
