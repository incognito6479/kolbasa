from django.urls import path
from .views import IncomeCreateView, IncomeListView, IncomeUpdateView, IncomeDetailView, \
    IncomeActionView

urlpatterns = [
    path('income/income_create/', IncomeCreateView.as_view(), name='income_create'),
    path('income/income_list/', IncomeListView.as_view(), name='income_list'),
    path('income/income_update/<int:pk>/', IncomeUpdateView.as_view(), name='income_update'),
    path('income/income_detail/<int:pk>/', IncomeDetailView.as_view(), name='income_detail'),
    path('income/income_action/<int:pk>', IncomeActionView.as_view(), name='income_action'),
]
