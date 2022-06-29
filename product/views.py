from datetime import datetime

from django.db.models import ProtectedError, Sum, Q, F
from django.shortcuts import redirect, render
from django.urls import reverse, reverse_lazy
from django.views.generic import CreateView, UpdateView, DeleteView, TemplateView
from django.views import View
from django.contrib.auth import authenticate, login, logout

from income.models import Income, IncomeItem
from order.models import ReturnItem, InvoiceItem, RetailOrderItem
from product.models import ProductCategory, Product
from user.models import User
from warehouse.models import WarehouseProduct


class HomeView(View):
    def get(self, request):
        if request.user.is_authenticated:
            return render(request, 'crm/home.html')
        else:
            return redirect('user_login_view')


class UserLoginView(View):
    def get(self, request):
        if not request.user.is_authenticated:
            return render(request, 'crm/login.html')
        else:
            return redirect('home_view')

    def post(self, request):
        phone = request.POST.get('phone')
        password = request.POST.get('password')
        user = authenticate(username=phone, password=password)
        if user is not None:
            login(request, user)
            return redirect('home_view')
        return redirect('user_login_view')


class UserLogoutView(View):
    def get(self, request):
        logout(request)
        return redirect('user_login_view')


class ProductCategoryCreateView(CreateView):
    model = ProductCategory
    fields = 'title', 'parent_category', 'is_main', 'bonus'
    template_name = 'crm/product/category_create.html'
    success_url = reverse_lazy('product_category_create')

    def get_context_data(self, **kwargs):
        context = super(ProductCategoryCreateView, self).get_context_data(**kwargs)
        context['item_list'] = ProductCategory.objects.all()
        return context


class ProductCategoryUpdateView(UpdateView):
    model = ProductCategory
    fields = 'title', 'parent_category', 'is_main', 'bonus'
    template_name = 'crm/product/category_update.html'
    success_url = reverse_lazy('product_category_create')


class ProductCategoryDeleteView(DeleteView):
    model = ProductCategory
    success_url = reverse_lazy('product_category_create')

    def get(self, request, *args, **kwargs):
        try:
            return self.post(request, *args, **kwargs)
        except ProtectedError:
            print("PROTECTED ERROR")
            return redirect(reverse_lazy('product_category_create') + "?error=protectederror")


class ProductCreateView(CreateView):
    model = Product
    fields = 'title', 'category', 'discount', 'price', 'description', \
             'unit_type', 'photo', 'code'
    template_name = 'crm/product/create.html'

    def get_success_url(self):
        return reverse('product_create')

    def get_context_data(self, **kwargs):
        context = super(ProductCreateView, self).get_context_data(**kwargs)
        category = self.request.GET.get('category')
        search = self.request.GET.get('search')
        products = Product.objects.all()

        if category:
            products = products.filter(category_id=category)

        if search:
            products = products.filter(title__icontains=search)

        context['categories'] = ProductCategory.objects.all()
        context['item_list'] = products
        context['selected_category'] = category
        context['selected_search'] = search
        return context


class ProductUpdateView(UpdateView):
    model = Product
    fields = 'title', 'category', 'discount', 'price', 'description', \
             'unit_type', 'photo', 'code'
    template_name = 'crm/product/update.html'
    success_url = reverse_lazy('product_create')


class ProductDeleteView(DeleteView):
    model = Product

    def get_success_url(self):
        return reverse('product_create')

    def get(self, request, *args, **kwargs):
        try:
            return self.post(request, *args, **kwargs)
        except ProtectedError:
            print("PROTECTED ERROR")
            return redirect(reverse_lazy('product_create'))


class ProductReport(TemplateView):
    template_name = 'crm/product/product_report.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(ProductReport, self).get_context_data()
        warehouse_product = WarehouseProduct.objects \
            .select_related('product', 'product__category', 'warehouse').all()

        start_date = self.request.GET.get('start_date')
        end_date = self.request.GET.get('end_date')

        context['end_date'] = end_date
        context['start_date'] = start_date

        if start_date and end_date:
            start_date += ' 00:00:00'
            end_date += ' 23:59:59'
            warehouse_product = warehouse_product \
                .annotate(income_total=
                          Sum('product__incomeitem__count',
                              filter=Q(product__incomeitem__income__created__range=[
                                  start_date,
                                  end_date
                              ],
                                  product__incomeitem__income__warehouse=F('warehouse'),
                                  product__incomeitem__income__status='completed')),
                          return_item_total=
                          Sum('returnitem__count',
                              filter=Q(returnitem__created__range=[
                                  start_date,
                                  end_date
                              ])),
                          invoice_total=
                          Sum('orderitem__invoiceitem__count',
                              filter=Q(orderitem__invoiceitem__invoice__created__range=[
                                  start_date,
                                  end_date
                              ],
                                  orderitem__invoiceitem__invoice__status='delivered')),
                          retail_order_total=
                          Sum('retailorderitem__count',
                              filter=Q(retailorderitem__order__created__range=[
                                  start_date,
                                  end_date
                              ],
                                  retailorderitem__order__status='delivered')))
        else:
            today_start = datetime.today().date().strftime('%Y-%m-%d') + ' 00:00:00'
            today_end = datetime.today().date().strftime('%Y-%m-%d') + ' 23:59:59'
            warehouse_product = warehouse_product \
                .annotate(income_total=
                          Sum('product__incomeitem__count',
                              filter=Q(product__incomeitem__income__created__range=[
                                  today_start,
                                  today_end
                              ],
                                  product__incomeitem__income__warehouse=F('warehouse'),
                                  product__incomeitem__income__status='completed')),
                          return_item_total=
                          Sum('returnitem__count',
                              filter=Q(returnitem__created__range=[
                                  today_start,
                                  today_end
                              ])),
                          invoice_total=
                          Sum('orderitem__invoiceitem__count',
                              filter=Q(orderitem__invoiceitem__invoice__created__range=[
                                  today_start,
                                  today_end
                              ],
                                  orderitem__invoiceitem__invoice__status='delivered')),
                          retail_order_total=
                          Sum('retailorderitem__count',
                              filter=Q(retailorderitem__order__created__range=[
                                  today_start,
                                  today_end
                              ],
                                  retailorderitem__order__status='delivered')))

        context['warehouse_products'] = warehouse_product
        return context


class ProductDetailReport(TemplateView):
    template_name = 'crm/product/product_detail_report.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(ProductDetailReport, self).get_context_data()

        start_date = self.request.GET.get('start_date')
        end_date = self.request.GET.get('end_date')

        context['end_date'] = end_date
        context['start_date'] = start_date

        context['warehouse_product'] = WarehouseProduct.objects.get(pk=kwargs.get('pk'))

        if start_date and end_date:
            start_date += ' 00:00:00'
            end_date += ' 23:59:59'
            warehouse_product_income_items = IncomeItem.objects \
                .select_related('income', 'income__provider').filter(income__created__range=[
                start_date, end_date
            ])
            context['warehouse_product_income_items_total'] = warehouse_product_income_items \
                .aggregate(amount_count=Sum('count'), amount_total=Sum('total'))
            context['warehouse_product_income_items'] = warehouse_product_income_items
            warehouse_product_return_items = ReturnItem.objects \
                .select_related('deliver', 'deliver__user').filter(created__range=[
                start_date, end_date
            ])
            context['warehouse_product_return_items_total'] = warehouse_product_return_items\
                .aggregate(amount_count=Sum('count'), amount_returned_count=Sum('returned_count'),
                           amount_total=Sum('total'))
            context['warehouse_product_return_items'] = warehouse_product_return_items
            warehouse_product_invoice_items = InvoiceItem.objects \
                .select_related('invoice__order', 'invoice', 'invoice__order__counter_party') \
                .filter(invoice__created__range=[
                start_date, end_date
            ])
            context['warehouse_product_invoice_items_total'] = warehouse_product_invoice_items\
                .aggregate(amount_count=Sum('count'), amount_total=Sum('total'))
            context['warehouse_product_invoice_items'] = warehouse_product_invoice_items
            warehouse_product_retail_items = RetailOrderItem.objects \
                .select_related('order', 'order__client').filter(order__created__range=[
                start_date, end_date
            ])
            context['warehouse_product_retail_items_total'] = warehouse_product_retail_items\
                .aggregate(amount_count=Sum('count'), amount_total=Sum('total'))
            context['warehouse_product_retail_items'] = warehouse_product_retail_items
        else:
            today_start = datetime.today().date().strftime('%Y-%m-%d') + ' 00:00:00'
            today_end = datetime.today().date().strftime('%Y-%m-%d') + ' 23:59:59'
            warehouse_product_income_items = IncomeItem.objects \
                .select_related('income', 'income__provider').filter(income__created__range=[
                today_start, today_end
            ])
            context['warehouse_product_income_items_total'] = warehouse_product_income_items \
                .aggregate(amount_count=Sum('count'), amount_total=Sum('total'))
            context['warehouse_product_income_items'] = warehouse_product_income_items
            warehouse_product_return_items = ReturnItem.objects \
                .select_related('deliver', 'deliver__user').filter(created__range=[
                today_start, today_end
            ])
            context['warehouse_product_return_items_total'] = warehouse_product_return_items\
                .aggregate(amount_count=Sum('count'), amount_returned_count=Sum('returned_count'),
                           amount_total=Sum('total'))
            context['warehouse_product_return_items'] = warehouse_product_return_items
            warehouse_product_invoice_items = InvoiceItem.objects \
                .select_related('invoice__order', 'invoice', 'invoice__order__counter_party') \
                .filter(invoice__created__range=[
                today_start, today_end
            ])
            context['warehouse_product_invoice_items_total'] = warehouse_product_invoice_items \
                .aggregate(amount_count=Sum('count'), amount_total=Sum('total'))
            context['warehouse_product_invoice_items'] = warehouse_product_invoice_items
            warehouse_product_retail_items = RetailOrderItem.objects \
                .select_related('order', 'order__client').filter(order__created__range=[
                today_start, today_end
            ])
            context['warehouse_product_retail_items_total'] = warehouse_product_retail_items \
                .aggregate(amount_count=Sum('count'), amount_total=Sum('total'))
            context['warehouse_product_retail_items'] = warehouse_product_retail_items

        return context
