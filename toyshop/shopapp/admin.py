from django.contrib import admin
from django.utils.safestring import mark_safe
# Register your models here.
from .models import Category, Product, Basket

#Отобразить продукты в категориях по категориям
class ProductInCategories(admin.TabularInline):
    model = Product
    extra = 0

#Модель категория товаров
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id','name','slug','photo',)
    inlines = [ProductInCategories]
    list_display_links = ('name',)
    search_fields = ('id','name',)
    search_help_text = ('Поиск по категориям')
    prepopulated_fields = {'slug': ('name',)}
#Метод отображения фото
    def get_html_photo(self, object):
        if object.photo:
            return mark_safe(f"<img src='{object.photo.url}' width=35>")
    get_html_photo.short_description = 'Фото'
admin.site.register(Category,CategoryAdmin)


#Модель продукты
class ProductAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'slug','is_sells', 'photo','category')
    list_display_links = ('name',)
    list_filter = ('category',)
    search_fields = ('id', 'name',)
    search_help_text = ('Поиск по товарам')
    prepopulated_fields = {'slug': ('name',)}

    # Метод отображения фото
    def get_html_photo(self, object):
        if object.photo:
            return mark_safe(f"<img src='{object.photo.url}' width=35>")
    get_html_photo.short_description = 'Фото'
admin.site.register(Product, ProductAdmin)

#Модель корзина покупок
class BasketAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'product', 'countProduct', 'priceProduct','fullSumm', 'time_create','time_update','is_buy')
    list_display_links = ('user','product',)
    list_filter = ('user',)
    search_fields = ('user', 'product',)
    search_help_text = ('Поиск по корзине')
admin.site.register(Basket, BasketAdmin)


admin.site.site_title = 'Панель администратора сайта'
admin.site.site_header = 'Панель администратора сайта'