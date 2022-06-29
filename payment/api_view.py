from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import status, viewsets, filters
from rest_framework.parsers import MultiPartParser
from rest_framework.response import Response
from rest_framework.views import APIView

from counter_party.helpers import counter_party_balance_income
from counter_party.models import CounterParty
from payment.filters import PaymentLogFilter
from payment.models import Outlay, PaymentLog
from payment.serializers import PaymentLogSerializer
from product.api_view import CustomPagination


class PaymentFromDeliverViewSet(viewsets.ModelViewSet):
    queryset = PaymentLog.objects.filter()
    serializer_class = PaymentLogSerializer
    filter_class = PaymentLogFilter
    pagination_class = CustomPagination
    filter_backends = (
        filters.OrderingFilter,
        DjangoFilterBackend,
        filters.SearchFilter
    )

    def create(self, request, *args, **kwargs):
        payment_serializer = self.get_serializer(data=request.data)
        counter_party_id = request.data.get('counter_party')
        user_id = request.data.get('user')
        payment_method = request.data.get('payment_method')
        outcat = 'counter_party'
        outlay, created = Outlay.objects.get_or_create(outcat='counter_party',
                                                       title='Выплата для погашения долга')
        if created:
            outlay = created
        amount = int(request.data.get('amount'))
        payment_type = 'income'
        try:
            PaymentLog.objects.create(user_id=user_id,
                                      outcat=outcat,
                                      model_id=counter_party_id,
                                      outlay=outlay,
                                      payment_type=payment_type,
                                      payment_method=payment_method,
                                      amount=amount)
        except CounterParty.DoesNotExist:
            return Response(status=status.HTTP_400_BAD_REQUEST, data={'massage': 'Клиент не найдено',
                                                                      'counter_party_id': counter_party_id})

        payment_serializer.is_valid()
        headers = self.get_success_headers(payment_serializer.data)
        return Response(payment_serializer.data, status=status.HTTP_201_CREATED, headers=headers)


# class CreatePaymentFromDelivers(APIView):
#     http_method_names = ['post']
#     parser_classes = (MultiPartParser,)
#
#     def post(self, request, format=None):
#         counter_party_id = request.POST.get('counter_party')
#         user_id = request.POST.get('user')
#         payment_method = request.POST.get('payment_method')
#         outcat = 'counter_party'
#         outlay, created = Outlay.objects.get_or_create(outcat='counter_party',
#                                                        title='Выплата для погашения долга')
#         if created:
#             outlay = created
#         amount = int(request.POST.get('amount'))
#         payment_type = 'income'
#         try:
#             counter_party_modal = CounterParty.objects.get(id=counter_party_id)
#             counter_party_balance_income(counter_party_id, amount)
#             PaymentLog.objects.create(user_id=user_id,
#                                       outcat=outcat,
#                                       model_id=counter_party_id,
#                                       outlay=outlay,
#                                       payment_type=payment_type,
#                                       payment_method=payment_method,
#                                       amount=amount)
#         except CounterParty.DoesNotExist:
#             return Response(status=status.HTTP_400_BAD_REQUEST, data={'massage': 'Клиент не найдено',
#                                                                       'counter_party_id': counter_party_id})
#
#         return Response(status=status.HTTP_200_OK, data={'massage': 'Оплата успешно проведено',
#                                                          'counter_party_id': counter_party_id,
#                                                          'amount': amount})
