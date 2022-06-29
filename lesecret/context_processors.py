class UrlController:
    def __init__(self, **kwargs):
        self.__dict__.update(kwargs)


def get_url_pattern(request):
    url_dict = {
        'product': ['product_category_create', 'product_category_update', 'product_category_delete',
                    'product_create', 'product_update', 'product_delete', 'product_report', 'product_detail_report'],
        'user': ['user_list', 'user_create', 'user_update', 'user_password_update', 'user_report'],
        'reports': ['payment_real_income', 'payment_theory_income'],
        'payment_real_income': ['payment_real_income'],
        'payment_theory_income': ['payment_theory_income'],
        'provider': ['provider_create', 'provider_update', 'provider_delete',
                     'order_invoice_provider_create', 'order_invoice_provider_update'],
        'provider_create': ['provider_create', 'provider_update', 'provider_delete'],
        'order_invoice_provider_create': ['order_invoice_provider_create', 'order_invoice_provider_update'],
        'counter_party': ['counter_party_list', 'counter_party_update', 'counter_party_delete',
                          'retail_client_list', 'retail_client_create', 'retail_client_update',
                          'retail_client_detail'],
        'counter_party_list': ['counter_party_list', 'counter_party_update', 'counter_party_report',
                               'counter_party_delete'],
        'retail_client_list': ['retail_client_list', 'retail_client_create', 'retail_client_update',
                               'retail_client_detail', 'retail_client_report'],
        'payment': ['payment_treatment', 'payment_list'],
        'payment_treatment': ['payment_treatment'],
        'payment_list': ['payment_list'],
        'movement': ['movement_list', 'movement_create', 'movement_detail', 'movement_update'],
        'order': ['order_list', 'order_update', 'order_detail', 'order_delete', 'order_actions',
                  'retail_order_list', 'retail_order_create', 'retail_order_update', 'retail_order_detail'],
        'order_list': ['order_list', 'order_update', 'order_detail', 'order_delete', 'order_actions'],
        'retail_order_list': ['retail_order_list', 'retail_order_create', 'retail_order_update', 'retail_order_detail'],
        'warehouse': ['warehouse_create', 'warehouse_update', 'warehouse_delete', 'warehouse_detail',
                      'return_items'],
        'warehouse_create': ['warehouse_create', 'warehouse_update', 'warehouse_delete', 'warehouse_detail'],
        'return_items': ['return_items'],
        'income': ['income_create', 'income_list', 'income_update',
                   'income_detail', 'income_action'],
        'product_report': ['product_report', 'product_detail_report'],
        'product_create': ['product_create', 'product_update', 'product_delete'],
        'product_category_create': ['product_category_create', 'product_category_update', 'product_category_delete'],
    }
    context = {
        'url_pattern': UrlController(**url_dict)
    }
    return context
