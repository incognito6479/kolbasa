from rest_framework import serializers

from counter_party.api_view import CounterPartySerializer
from counter_party.models import CounterParty
from payment.models import PaymentLog, Outlay
from user.serializers import UserSerializer


class OutlaySerializer(serializers.ModelSerializer):

    class Meta:
        model = Outlay
        fields = 'id', 'title', 'outcat'


class PaymentLogSerializer(serializers.ModelSerializer):
    user_objs = UserSerializer(many=False, read_only=True, source='user')
    outlay_objs = OutlaySerializer(many=False, read_only=True, source='outlay')
    counter_party_obj = serializers.SerializerMethodField()

    class Meta:
        model = PaymentLog
        fields = 'id', 'created', 'outcat', 'model_id', 'outlay_objs', \
                 'payment_type', 'payment_method', 'amount', 'user_objs', 'counter_party_obj'

    def get_counter_party_obj(self, obj):
        try:
            return CounterPartySerializer(CounterParty.objects.get(id=obj.model_id), many=False).data
        except CounterParty.DoesNotExist:
            return 'Клиент не найдено'
