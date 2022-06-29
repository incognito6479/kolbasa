from django.urls import path
from rest_framework import routers

from payment.api_view import PaymentFromDeliverViewSet
from payment.views import PaymentTreatment, PaymentAction, PaymentLogListView, PaymentIncomeReal, PaymentIncomeTheory, \
    payment_theory_report_excel, payment_real_excel_download

router = routers.SimpleRouter()
router.register(r'payments', PaymentFromDeliverViewSet)

urlpatterns = [
    path('payment_treatment/', PaymentTreatment.as_view(), name='payment_treatment'),
    path('payment_list/', PaymentLogListView.as_view(), name='payment_list'),
    path('payment_action/', PaymentAction.as_view(), name='payment_action'),
    path('payment_real_income/', PaymentIncomeReal.as_view(), name='payment_real_income'),
    path('payment_real_income/excel/', payment_real_excel_download, name='payment_real_income_excel'),
    path('payment_theory_income/', PaymentIncomeTheory.as_view(), name='payment_theory_income'),
    path('payment_theory_income/excel/', payment_theory_report_excel, name='payment_theory_income_excel'),
]
