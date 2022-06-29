from rest_framework import serializers
from product.models import Product
from user.models import User


class ProductSerializer(serializers.ModelSerializer):
	class Meta:
		model = Product
		fields = '__all__'


class UserSerializer(serializers.ModelSerializer):
	class Meta:
		model = User
		fields = ['id', 'username', 'fullname', 'user_region', 'user_type']