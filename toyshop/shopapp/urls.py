from django.urls import path, include

from shopapp.views import index, CategoryShow, CatalogShow, ShowProduct, RegistrationUser, LoginUser, logout_user, FormReviewProduct, \
    aboutList, addMyBasket, MyBasket, dellProductFromBasket

urlpatterns = [
    path('',index, name='home'),
    path('catalog/',CatalogShow.as_view(), name='catalog'),#каталог все товары
    path('category/<slug:slug>',CategoryShow.as_view(), name='category'),#товары в разрезе категории
    path('product/<slug:slug>',ShowProduct.as_view(), name='product'),#продукт
    path('register/',RegistrationUser.as_view(), name='register'),#Регистрация
    path('login/',LoginUser.as_view(), name='login'),#Авторизация
    path('logout/',logout_user,name='logout'),#Выйти из авторизации
    path('review/<slug:slug>', FormReviewProduct.as_view(),name='review'),#Страница отзыв о товаре с формой!
    path('about/',aboutList,name="about"),#страница о нас
    path('mybasket/<int:id>', addMyBasket, name='mybasket'),#добавление товара в корзину
    path('mybasket/', MyBasket.as_view(), name='basket'),#Корзина покупок
    path('dellbasket/<int:id>', dellProductFromBasket, name='dellbasket'),#Удаление из корзины
]
