from django_filters import FilterSet, RangeFilter, DateTimeFromToRangeFilter

from counter_party.models import CounterParty
from order.models import Order, Invoice


class OrderFilter(FilterSet):
    created_range = RangeFilter(field_name='created')

    class Meta:
        model = Order
        fields = ('counter_party', 'created_range', 'status', 'agent__user')


class InvoiceFilter(FilterSet):
    created_range = DateTimeFromToRangeFilter(field_name='order__created')

    class Meta:
        model = Invoice
        fields = ('deliver__user', 'deliver__user__user_region', 'order__agent__user', 'status')


class CounterPartyForReturnItemFilter(FilterSet):

    class Meta:
        model = CounterParty
        fields = ('return_items__deliver__user', 'id')
