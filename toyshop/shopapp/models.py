
from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User
from django.core.validators import EmailValidator, RegexValidator
from django.core.exceptions import ValidationError

# Create your models here.

#-------------------------------
class Category(models.Model):#Категория товаров
    name = models.CharField(max_length=30, verbose_name='Название категории')
    slug = models.SlugField(max_length=30, verbose_name='URL- категории')
    photo = models.ImageField(upload_to=f'photos/', verbose_name='Фото категории')
    def __str__(self):#Строковое представление модели
        return f'{self.name}'
    def get_absolute_url(self):#ссылка на категорию - как метод
        return reverse('category', kwargs={'slug':self.slug})
    class Meta:# Вложенный класс - для админки
        verbose_name = 'Категория'  # ед
        verbose_name_plural = 'Категории'  # множ
        ordering = ['name']

#------------------------------------------
class Product(models.Model):#Модель товары
    name = models.CharField(max_length=50, verbose_name='Название товара')
    slug = models.SlugField(max_length=50, verbose_name='URL- товара')
    price = models.IntegerField(verbose_name='Цена товара')
    is_sells = models.BooleanField(verbose_name='В продаже')
    photo = models.ImageField(upload_to=f'photos/products/', verbose_name='Фото товара')
    category = models.ForeignKey(Category, on_delete=models.CASCADE, null=True, blank=False, verbose_name='Категория')
    def __str__(self):#Строковое представление модели
        return f'{self.name}'
    def get_absolute_url(self):#ссылка на товар - как метод
        return reverse('product', kwargs={'slug':self.slug})
    class Meta:# Вложенный класс - для админки
        verbose_name = 'Продукт'  # ед
        verbose_name_plural = 'Продукты'  # множ
        ordering = ['name','price','is_sells']

#--------------------------------------------------
class Review(models.Model):#Модель отзыв о товаре - к ней форма!!!!
    reviewText = models.TextField(max_length=1000)
    product = models.ForeignKey(Product,  on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    time_create = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')
    class Meta:
        verbose_name = 'Отзыв'  # ед
        verbose_name_plural = 'Отзывы'  # множ
        ordering = ['product','user','time_create']

#-----------------------------------------------
class Subscribers(models.Model):#Модель подписчики на скидку - к ней форма!!!!
    name = models.CharField(max_length=30)
    email = models.EmailField()
    tell = models.CharField(max_length=20)

#-----------------------------Модель для корзины покупок-------------------#

class Basket(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Покупатель')
    product = models.ForeignKey(Product, on_delete=models.CASCADE,verbose_name='Продукт')
    countProduct = models.SmallIntegerField(verbose_name='Кол-во в заказе',default=1) #Реализовать на странице форму +/-
    priceProduct = models.IntegerField(verbose_name='Цена за шт')
    fullSumm = models.IntegerField(verbose_name='Сумма итого')
    time_create = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')
    time_update = models.DateTimeField(auto_now=True, verbose_name='Дата обновления')
    is_buy = models.BooleanField(default=True, verbose_name='Оплачен')
    def __str__(self):#Строковое представление
        return f'Покупатель: {self.user} продукт {self.product}'
    def __iadd__(self, other=1):#Добавление кол-ва товара
        self.countProduct +=other
        return self.countProduct
    def fullSummProduct(self):
        self.fullSumm = self.countProduct * self.priceProduct
        return f'{self.fullSumm}'
    class Meta:
        verbose_name = 'Корзина'  # ед
        verbose_name_plural = 'Корзина'  # множ
        ordering = ['user','is_buy','time_create']







