from django.db import models

from product.choices import PRODUCT_UNIT_TYPE


class ProductCategory(models.Model):
    title = models.CharField(max_length=255,
                             verbose_name='Название категории')
    parent_category = models.ForeignKey('self',
                                        verbose_name='Родительская категория',
                                        related_name='parent',
                                        on_delete=models.CASCADE,
                                        null=True,
                                        blank=True)
    is_main = models.BooleanField(default=False,
                                  verbose_name='Главная категория')
    bonus = models.BooleanField(default=False, verbose_name='Бонусная')

    def __str__(self):
        return self.title


class Product(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    category = models.ForeignKey('product.ProductCategory',
                                 verbose_name='Категория Товара',
                                 on_delete=models.PROTECT)
    title = models.CharField(max_length=255,
                             verbose_name='Наименование товара')
    code = models.CharField(max_length=255, default='',
                            verbose_name='Код')
    discount = models.FloatField(default=0, verbose_name='Скидка')
    photo = models.ImageField(verbose_name='Фото', upload_to='product_photo',
                              default='../static/crm/images/no-image.png')
    price = models.IntegerField(default=0, verbose_name='Цена')
    show_price = models.IntegerField(default=0, verbose_name='Цена со скидкой')
    description = models.TextField(null=True, blank=True, verbose_name='Описание товара')
    unit_type = models.CharField(max_length=255, choices=PRODUCT_UNIT_TYPE,
                                 verbose_name='Единица измерения')

    def __str__(self):
        return self.title

    def save(self, force_insert=False, force_update=False, using=None,
             update_fields=None):
        self.show_price = self.price - self.discount
        super(Product, self).save()
