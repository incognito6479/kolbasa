from django_filters import FilterSet
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets, serializers, filters, status
from rest_framework.response import Response

from counter_party.models import CounterParty
from product.api_view import CustomPagination
from user.models import User


class CounterPartyFilter(FilterSet):
    class Meta:
        model = CounterParty
        fields = ['region']


class CounterPartySerializer(serializers.ModelSerializer):
    phone_number = serializers.SerializerMethodField()
    marker = serializers.SerializerMethodField()

    class Meta:
        model = CounterParty
        fields = 'id', 'full_name', 'phone_number', 'address', 'landmark', 'region', 'content', 'balance', 'marker'

    def get_phone_number(self, obj):
        if obj.phone_number:
            return obj.phone_number.split(',')
        else:
            return []

    def get_marker(self, obj):
        if obj.marker:
            return [float(x) for x in obj.marker.split(',')]
        else:
            return []


class CounterPartyViewSet(viewsets.ModelViewSet):
    queryset = CounterParty.objects.all()
    serializer_class = CounterPartySerializer
    filter_class = CounterPartyFilter
    pagination_class = CustomPagination
    filter_backends = (
        filters.OrderingFilter,
        DjangoFilterBackend,
        filters.SearchFilter
    )

    def create(self, request, *args, **kwargs):
        # longitude and latitude
        request.data['marker'] = ','.join((str(i) for i in request.data.pop('marker')))
        request.data['phone_number'] = ','.join((str(i) for i in request.data.pop('phone_number')))
        counter_party_serializer = self.get_serializer(data=request.data)

        counter_party, created = CounterParty.objects.get_or_create(full_name=request.data.get('full_name'),
                                                                    phone_number=request.data.get('phone_number'),
                                                                    defaults={
                                                                        'marker': request.data['marker'],
                                                                        'address': request.data.get('address'),
                                                                        'region': request.data.get('region'),
                                                                        'content': request.data.get('content', ''),
                                                                        'landmark': request.data.get('landmark', ''),
                                                                    }
                                                                    )
        if created:
            counter_party_serializer.is_valid()
            return Response({'Ok': 'Ok'}, status=status.HTTP_201_CREATED)
        else:
            counter_party.marker = request.data['marker']
            counter_party.save()
            counter_party_serializer.is_valid()
            return Response({'counter_party_duplicate': 'Ok'}, status=status.HTTP_200_OK)
