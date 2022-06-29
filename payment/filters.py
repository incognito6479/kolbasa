from django_filters import FilterSet

from payment.models import PaymentLog


class PaymentLogFilter(FilterSet):

    class Meta:
        model = PaymentLog
        fields = ('user', 'model_id', 'status')
