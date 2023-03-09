
from django.contrib.auth.models import User
from django.contrib.auth.views import LoginView
from django.http import request
from django.shortcuts import render, HttpResponse,reverse, redirect
from django.contrib.auth import authenticate, login,logout
from django.urls import reverse_lazy
from .models import Category, Product, Review, Basket
from django.views.generic import TemplateView, View, ListView, DetailView, CreateView, FormView
from .forms import SubscribersForm, RegisterUserForm, LoginUserForm, FormReview, BasketForm
from datetime import datetime

# Create your views here.


#-------------------
def index(request):#Главная Страница
    if request.method == 'POST':
        form = SubscribersForm(request.POST)
        if form.is_valid():
            try:
                print(form.cleaned_data)
                form.save()
                return redirect('home')
            except:
                form.add_error(None, 'Ошибка отправления данных')
    else:
        title = 'Главная страница сайта'
        form = SubscribersForm()
        category = Category.objects.all()
        productsStaff = Product.objects.filter(category__name='Stuffed Animals', is_sells=True)[:4]
        productsWooden = Product.objects.filter(category__name='Wooden Toys', is_sells=True)[:4]
        contextData = {
        'title':title,
        'category':category,
        'productsStaff':productsStaff,
        'productsWooden':productsWooden,
        'form':form,

        }
        print(request.user.username, request.user.groups, request.user.user_permissions)
        return render(request, 'shopapp/index.html', context=contextData)

#----------------
class CategoryShow(DetailView):#Отобразить товары по категории
    model = Category
    template_name = 'shopapp/category.html'
    slug_url_kwarg = 'slug'
    context_object_name = 'cat'
    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = f'Группа {self.context_object_name}'
        context['form'] = BasketForm()
        return context
    def form_valid(self,context):
        print(context)
        print(self.request.POST)
        print(self.request.user.username)
        return redirect('catalog')
# def catalog(request):
#     title = 'Каталог сайта'
#     contextData = {
#         'title':title,
#     }
#     return render(request, 'shopapp/catalog.html', context=contextData)
#---------------
class CatalogShow(FormView):#Отобразить каталог товаров
    form_class = BasketForm
    template_name = 'shopapp/catalog.html'
    success_url = reverse_lazy('catalog')
    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['cat'] = Category.objects.all()
        context['title'] = f'Каталог товаров'
        return context
    def form_valid(self,form):
        print(self.request.POST)
        return redirect('catalog')


#-----------
class ShowProduct(DetailView):#Просмотр карточки продукта
    model = Product
    template_name = 'shopapp/product.html'
    slug_url_kwarg = 'slug'
    context_object_name = 'product'
    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = f'{self.context_object_name}'
        return context

#------------
class FormReviewProduct(FormView):#Форма оставить отзыв о товаре
    form_class = FormReview
    template_name = 'shopapp/review.html'
    slug_url_kwarg = 'slug'
    success_url = reverse_lazy('catalog')
    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['product'] = Product.objects.get(slug=self.kwargs['slug'])
        name = context['product']
        context['title'] = f'{name}'
        return context
    def form_valid(self, context):#функция передаци данных из формы и внесение в бд данных об отзыве
        review = Review()
        review.reviewText = self.request.POST.get('reviewText')
        review.product = Product.objects.get(slug=self.kwargs['slug'])
        review.user = User.objects.get(id=self.request.user.id)
        review.time_create = datetime.now()
        review.save()
        return redirect('catalog')

#---------------
def aboutList(request):
    title = 'О нас'
    contextData = {
        'title':title,
    }
    return render(request,  'shopapp/about.html', context=contextData)

#---------- Регистрация пользователей - страница с формой на основе базового шаблона плюс свой

class RegistrationUser(CreateView):
    form_class = RegisterUserForm
    template_name = 'shopapp/register.html'
    success_url = reverse_lazy('login')
    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Страница регистраиции пользователя'
        return context
    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return reverse_lazy('home')

#Авторизация пользователя
class LoginUser(LoginView):
    form_class = LoginUserForm  # стандартная форма авторизации
    template_name = 'shopapp/login.html'
    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Страница авторизации пользователя'
        return context
    def get_success_url(self):
        return reverse_lazy('home')

#Выход из авторизации
def logout_user(request):
    logout(request)#Стандартная функция выхода
    return redirect('login')

#Функция добавление в корзину
def addMyBasket(request, id):
    if request.method == "POST":
        basket = Basket()
        product = Product.objects.get(id=id)
        basket.user = User.objects.get(id=request.user.id)
        basket.product = Product.objects.get(id=id)
        basket.priceProduct = product.price
        basket.countProduct = request.POST.get('countProduct')
        basket.fullSumm = int(product.price) * int(request.POST.get('countProduct'))
        basket.save()
    return redirect('home')

#user = User.objects.get(username=request.user)
#basket = user.basket_set.filter(user__id=user.id)

class MyBasket(ListView):#Класс отображение корзины покупок
    model = Basket
    template_name = "shopapp/mybasket.html"
    context_object_name = 'products'
    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['user'] = User.objects.get(id=self.request.user.id)
        context['fullSum'] = Basket.objects.filter(user__id=self.request.user.id)
        context['title'] = 'Корзина покупок'
        print(context['fullSum'])
        return context

#--------Удаление товара из корзины
def dellProductFromBasket(request,id):
    try:
        product = Basket.objects.get(id=id)
        product.delete()
        return  redirect('basket')
    except:
        return redirect('basket')