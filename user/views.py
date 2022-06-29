from datetime import datetime

from django.contrib.auth.forms import PasswordChangeForm, SetPasswordForm
from django.db.models import Sum
from django.shortcuts import redirect
from django.urls import reverse
from django.views.generic import ListView, CreateView, UpdateView, TemplateView
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework import exceptions

from order.models import Invoice
from payment.models import PaymentLog
from product.models import Product
from user.choices import marker_data
from user.forms import UserCreateForm, UserUpdateForm
from user.serializers import ProductSerializer, UserSerializer
from user.helpers import get_tokens_for_user, add_payment
from user.models import User, Agent, Deliver


class UserLoginView(APIView):
    permission_classes = (AllowAny,)

    def post(self, request):
        phone = request.POST.get('username')
        password = request.POST.get('password')

        if (phone is None) or (password is None):
            raise exceptions.AuthenticationFailed('username and password required')

        user = User.objects.filter(username=phone).first()

        if (user is None):
            raise exceptions.AuthenticationFailed('user not found')

        if (not user.check_password(password)):
            raise exceptions.AuthenticationFailed('wrong password')

        access_token = get_tokens_for_user(user)

        serialized_user = UserSerializer(user)
        user_data = serialized_user.data
        user_data['region_coordinates'] = (marker_data[user_data['user_region']][0],
                                           marker_data[user_data['user_region']][1])
        user_data['region_coordinates_zoom'] = marker_data[user_data['user_region']][2]
        context = {
            'access': access_token,
            'user': user_data,
        }
        return Response(context)


class UserListView(ListView):
    model = User
    context_object_name = 'users'
    template_name = 'crm/user/user_list.html'
    paginate_by = 25

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(UserListView, self).get_context_data()
        user_region = self.request.GET.get('user_region')
        user_type = self.request.GET.get('user_type')
        context['user_type'] = user_type
        context['user_region'] = user_region
        return context

    def get_queryset(self):
        orders = super(UserListView, self).get_queryset()

        user_type = self.request.GET.get('user_type')
        user_region = self.request.GET.get('user_region')

        if user_type:
            orders = orders.filter(user_type=user_type)
        else:
            orders = orders.filter(user_type__in=['agent', 'deliver'])

        if user_region:
            orders = orders.filter(user_region=user_region)

        return orders


class UserCreateView(CreateView):
    model = User
    form_class = UserCreateForm
    template_name = 'crm/user/user_create.html'
    success_url = '/user_list/'

    def get_form(self, form_class=None):
        form_class = super(UserCreateView, self).get_form(form_class)
        form_class.fields['password1'].label = 'Пароль'
        form_class.fields['password2'].label = 'Повтарите пароль'
        new_user_type_choices = list()
        for choice in form_class.fields['user_type'].choices:
            if choice[0] == 'agent' or choice[0] == 'deliver':
                new_user_type_choices.append(choice)
        form_class.fields['user_type'].choices = new_user_type_choices
        return form_class

    def form_valid(self, form):
        form.instance.is_active = True
        success_url = super(UserCreateView, self).form_valid(form)
        if form.data['user_type'] == 'agent':
            Agent.objects.create(user=self.object, service_percent=form.data['service_percent'])
        elif form.data['user_type'] == 'deliver':
            Deliver.objects.create(user=self.object, service_percent=form.data['service_percent'])
        return success_url


class UserUpdateView(UpdateView):
    model = User
    template_name = 'crm/user/user_update.html'
    success_url = '/user_list/'
    form_class = UserUpdateForm

    def form_valid(self, form):
        if form.instance.user_type == 'agent':
            Agent.objects.filter(user=self.object) \
                .update(service_percent=form.data['service_percent'])
        elif form.instance.user_type == 'deliver':
            Deliver.objects.filter(user=self.object) \
                .update(service_percent=form.data['service_percent'])
        success_url = super(UserUpdateView, self).form_valid(form)
        return success_url


class UserPasswordUpdateView(UpdateView):
    model = User
    template_name = 'crm/user/user_update_password.html'
    success_url = '/user_list/'
    form_class = PasswordChangeForm

    def get_form(self, form_class=None):
        """Return an instance of the form to be used in this view."""
        user = User.objects.get(pk=self.kwargs['pk'])
        if form_class is None:
            form_class = self.get_form_class()
        return form_class(user)

    def form_valid(self, form):
        return super(UserPasswordUpdateView, self).form_valid(form)

    def form_invalid(self, form):
        if self.request.POST.get('new_password1') == self.request.POST.get('new_password2'):
            self.object.set_password(self.request.POST.get('new_password1'))
            return redirect(self.success_url)
        return super(UserPasswordUpdateView, self).form_invalid(form)


class UserReport(TemplateView):
    template_name = 'crm/user/user_report.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(UserReport, self).get_context_data()

        start_date = self.request.GET.get('start_date')
        end_date = self.request.GET.get('end_date')

        context['start_date'] = start_date
        context['end_date'] = end_date

        user_modal = User.objects.prefetch_related('agent').get(pk=kwargs.get('pk'))
        context['user_model'] = user_modal

        if user_modal.user_type == 'agent':
            context['user_agent_instance'] = Agent.objects.get(user=user_modal)
            if start_date and end_date:
                start_date += ' 00:00:00'
                end_date += ' 23:59:59'
                invoices = Invoice.objects.filter(order__agent__user=user_modal,
                                                  status='delivered',
                                                  created__range=[
                                                      start_date, end_date
                                                  ])
                context['invoices_total'] = invoices.aggregate(amount_total=Sum('total'))
                context['invoices'] = invoices
                payments = PaymentLog.objects.filter(outcat='user', model_id=user_modal.id)
                context['payments_total'] = payments.aggregate(amount_total=Sum('amount'))
                context['payments'] = payments
            else:
                today_start = datetime.today().date().strftime('%Y-%m-%d') + ' 00:00:00'
                today_end = datetime.today().date().strftime('%Y-%m-%d') + ' 23:59:59'
                invoices = Invoice.objects.filter(order__agent__user=user_modal,
                                                  status='delivered',
                                                  created__range=[
                                                      today_start, today_end
                                                  ])
                context['invoices_total'] = invoices.aggregate(amount_total=Sum('total'))
                context['invoices'] = invoices
                payments = PaymentLog.objects.filter(outcat='user', model_id=user_modal.id)
                context['payments_total'] = payments.aggregate(amount_total=Sum('amount'))
                context['payments'] = payments
        elif user_modal.user_type == 'deliver':
            context['user_deliver_instance'] = Deliver.objects.get(user=user_modal)
            if start_date and end_date:
                start_date += ' 00:00:00'
                end_date += ' 23:59:59'
                invoices = Invoice.objects.filter(deliver__user=user_modal,
                                                  status='delivered',
                                                  created__range=[
                                                      start_date, end_date
                                                  ])
                context['invoices_total'] = invoices.aggregate(amount_total=Sum('total'))
                context['invoices'] = invoices
                payments = PaymentLog.objects.filter(outcat='user', model_id=user_modal.id,
                                                     created__range=[
                                                         start_date, end_date
                                                     ])
                context['payments_total'] = payments.aggregate(amount_total=Sum('amount'))
                context['payments'] = payments
            else:
                today_start = datetime.today().date().strftime('%Y-%m-%d') + ' 00:00:00'
                today_end = datetime.today().date().strftime('%Y-%m-%d') + ' 23:59:59'
                invoices = Invoice.objects.filter(deliver__user=user_modal,
                                                  status='delivered',
                                                  created__range=[
                                                      today_start, today_end
                                                  ])
                context['invoices_total'] = invoices.aggregate(amount_total=Sum('total'))
                context['invoices'] = invoices
                payments = PaymentLog.objects.filter(outcat='user', model_id=user_modal.id,
                                                     created__range=[
                                                         today_start, today_end
                                                     ])
                context['payments_total'] = payments.aggregate(amount_total=Sum('amount'))
                context['payments'] = payments
        return context

    def post(self, request, pk):
        action = request.POST.get('action', None)
        actions = {
            'add_payment': add_payment
        }
        actions[action](request, self.kwargs)
        return redirect(reverse('user_report', kwargs={'pk': self.kwargs['pk']}))
