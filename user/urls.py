from django.urls import path
from user.views import UserLoginView, UserListView, UserCreateView, UserUpdateView, UserPasswordUpdateView, UserReport

urlpatterns = [
	path('api/v1/token/', UserLoginView.as_view(), name='token_obtain_pair'),
	path('user_list/', UserListView.as_view(), name='user_list'),
	path('user_create/', UserCreateView.as_view(), name='user_create'),
	path('user_update/<int:pk>/', UserUpdateView.as_view(), name='user_update'),
	path('user_report/<int:pk>/', UserReport.as_view(), name='user_report'),
	path('user_password_update/<int:pk>/', UserPasswordUpdateView.as_view(), name='user_password_update'),
]
