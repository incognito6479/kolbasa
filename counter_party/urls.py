from django.urls import path
from rest_framework import routers

from counter_party.api_view import CounterPartyViewSet
from counter_party.views import CounterPartyView, CounterPartyUpdateView, CounterPartydeleteView, ProviderCreateView, \
	ProviderUpdateView, ProviderDeleteView, RetailClientListView, RetailClientCreateView, RetailClientUpdateView, \
	RetailClientDetailView, RetailClientDeleteView, CounterPartyReport, RetailClientReport, retail_client_report_excel, \
	counter_party_report_excel

router = routers.SimpleRouter()
router.register(r'counter_party', CounterPartyViewSet)

urlpatterns = [
	path('counter_party/list/', CounterPartyView.as_view(), name="counter_party_list"),
	path('counter_party/update/<int:pk>', CounterPartyUpdateView.as_view(), name="counter_party_update"),
	path('counter_party/delete/<int:pk>', CounterPartydeleteView.as_view(), name="counter_party_delete"),
	path('counter_party/report/<int:pk>', CounterPartyReport.as_view(), name="counter_party_report"),
	path('counter_party/report/excel/<int:pk>', counter_party_report_excel, name="counter_party_report_excel"),
	path('provider/list/', ProviderCreateView.as_view(), name="provider_create"),
	path('provider/update/<int:pk>', ProviderUpdateView.as_view(), name="provider_update"),
	path('provider/delete/<int:pk>', ProviderDeleteView.as_view(), name="provider_delete"),

	path('retail_client/list/', RetailClientListView.as_view(), name='retail_client_list'),
	path('retail_client/create/', RetailClientCreateView.as_view(), name='retail_client_create'),
	path('retail_client/update/<int:pk>/', RetailClientUpdateView.as_view(), name='retail_client_update'),
	path('retail_client/detail/<int:pk>/', RetailClientDetailView.as_view(), name='retail_client_detail'),
	path('retail_client/delete/<int:pk>/', RetailClientDeleteView.as_view(), name='retail_client_delete'),
	path('retail_client/report/<int:pk>/', RetailClientReport.as_view(), name='retail_client_report'),
	path('retail_client/report/excel/<int:pk>/', retail_client_report_excel, name='retail_client_report_excel'),
]
