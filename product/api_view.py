from django_filters import FilterSet
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets, serializers, pagination, filters
from rest_framework.response import Response

from product.models import Product, ProductCategory
from warehouse.models import WarehouseProduct, Warehouse


class CustomPagination(pagination.PageNumberPagination):
    page_size_query_param = 'limit'

    def get_paginated_response(self, data):
        limit = self.request.GET.get('limit', self.page_size)
        next_page = None
        previous_page = None
        if self.page.has_next():
            next_page = self.page.next_page_number()
        if self.page.has_previous():
            previous_page = self.page.previous_page_number()
        return Response({
            'next': self.get_next_link(),
            'next_page': next_page,
            'previous': self.get_previous_link(),
            'previous_page': previous_page,
            'count': self.page.paginator.count,
            'limit': int(limit),
            'results': data,
        })


class WarehouseProductFilter(FilterSet):

    class Meta:
        model = WarehouseProduct
        fields = ['created']


class ProductCategorySerializer(serializers.ModelSerializer):

    class Meta:
        model = ProductCategory
        fields = 'id', 'is_main'


class ProductSerializer(serializers.ModelSerializer):
    category_obj = ProductCategorySerializer(many=False, read_only=True, source='category')

    class Meta:
        model = Product
        fields = 'id', 'created', 'category_obj', 'title',  'discount',  'show_price', \
                 'description', 'unit_type', 'photo', 'code'


class WarehouseSerializer(serializers.ModelSerializer):

    class Meta:
        model = Warehouse
        fields = 'id', 'name', 'address'


class WarehouseProductSerializer(serializers.ModelSerializer):
    product_obj = ProductSerializer(many=False, read_only=True, source='product')
    warehouse_obg = WarehouseSerializer(many=False, read_only=True, source='warehouse')

    class Meta:
        model = WarehouseProduct
        fields = 'id', 'created', 'warehouse_obg', 'product_obj',  'count'


class WarehouseProductViewSet(viewsets.ModelViewSet):
    queryset = WarehouseProduct.objects.all()
    serializer_class = WarehouseProductSerializer
    filter_class = WarehouseProductFilter
    pagination_class = CustomPagination
    filter_backends = (
        filters.OrderingFilter,
        DjangoFilterBackend,
        filters.SearchFilter
    )
