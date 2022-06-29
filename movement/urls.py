from django.urls import path
from .views import MovementCreateView, MovementListView, MovementDetailView, MovementUpdateView, \
	MovementActionsView


urlpatterns = [
	path('movement/movement_create/', MovementCreateView.as_view(), name='movement_create'),
	path('movement/movement_list/', MovementListView.as_view(), name='movement_list'),
	path('movement/movement_detail/<int:pk>', MovementDetailView.as_view(), name='movement_detail'),
	path('movement/movement_update/<int:pk>', MovementUpdateView.as_view(), name='movement_update'),
	path('movement/movement_action/<int:pk>', MovementActionsView.as_view(), name='movement_actions'),
]