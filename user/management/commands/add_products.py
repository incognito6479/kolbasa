import openpyxl
from django.core.management.base import BaseCommand

from product.models import Product


class Command(BaseCommand):
    help = 'Initialize base data for deploying'

    def handle(self, *args, **options):
        xl_doc = openpyxl.open('products.xlsx')
        sheet1 = xl_doc.worksheets[0]
        current_cat = 1
        for row in sheet1.rows:
            if row[0].value == 'cat2':
                current_cat = 3
                continue
            if row[0].value == 'cat3':
                current_cat = 4
                continue
            Product.objects.get_or_create(code=row[0].value,
                                          defaults={
                                              'category_id': current_cat,
                                              'title': row[1].value,
                                              'discount': 0,
                                              'price': 0,
                                              'show_price': 0,
                                              'unit_type': row[2].value
                                          })

        sheet2 = xl_doc.worksheets[1]
        current_cat = 2
        for row in sheet2.rows:
            Product.objects.get_or_create(code=row[0].value,
                                          defaults={
                                              'category_id': current_cat,
                                              'title': row[1].value,
                                              'discount': 0,
                                              'price': 0,
                                              'show_price': 0,
                                              'unit_type': row[2].value
                                          })
