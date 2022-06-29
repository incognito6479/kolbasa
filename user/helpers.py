from rest_framework_simplejwt.tokens import RefreshToken

from payment.helpers import payment_income_action, payment_outcome_action
from payment.models import Outlay
from user.models import User, Agent, Deliver


def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)

    return str(refresh.access_token)


def add_payment(request, kwargs):
    user_id = kwargs.get('pk')
    user_instance = User.objects.get(pk=user_id)
    payment_type = request.POST.get('payment_type')
    payment_method = request.POST.get('payment_method')
    amount = int(request.POST.get('amount'))
    outlay, created = Outlay.objects.get_or_create(outcat='retail_order',
                                                   title='Выплата для сотрудника')
    if payment_type == 'income':
        payment_income_action('user', user_id, outlay, payment_method, amount, request.user)
        if user_instance.user_type == 'agent':
            agent_instance = Agent.objects.get(user=user_instance)
            agent_instance.balance += amount
            agent_instance.save()
        if user_instance.user_type == 'deliver':
            deliver_instance = Deliver.objects.get(user=user_instance)
            deliver_instance.balance += amount
            deliver_instance.save()
    elif payment_type == 'outcome':
        payment_outcome_action('user', user_id, outlay, payment_method, amount, request.user)
        if user_instance.user_type == 'agent':
            agent_instance = Agent.objects.get(user=user_instance)
            agent_instance.balance -= amount
            agent_instance.save()
        if user_instance.user_type == 'deliver':
            deliver_instance = Deliver.objects.get(user=user_instance)
            deliver_instance.balance -= amount
            deliver_instance.save()
