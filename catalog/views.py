from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import ListView, TemplateView, DetailView, CreateView, UpdateView, DeleteView
from .models import Product, Contact, Category
from django.urls import reverse_lazy
from django.core.cache import cache
from django.http import HttpResponse

from .services import get_products_from_cache, get_products_by_category_from_cache, get_categories_from_cache


def my_view(request):
    # Попытка получить данные из кеша
    data = cache.get('my_key')

    # Если данные не найдены в кеше, выполняем вычисления и сохраняем результат в кеш
    if not data:
        data = 'some expensive computation'
        cache.set('my_key', data, 60 * 15)  # Кешируем данные на 15 минут

    # Возвращаем ответ с данными
    return HttpResponse(data)


class ProductsByCategoryListView(ListView):
    model = Product
    template_name = 'catalog/products_by_category.html'
    context_object_name = 'products'

    def get_queryset(self):
        # Получаем ID категории из URL-параметров
        category_pk = self.kwargs.get('pk')
        return get_products_by_category_from_cache(category_pk)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        category_pk = self.kwargs.get('pk')
        # Получаем название категории для заголовка
        try:
            category_name = Product.objects.filter(category_id=category_pk).first().category.name
        except AttributeError:
            category_name = "Неизвестная категория"

        context['title'] = f'Продукты в категории: {category_name}'
        return context


class ProductListView(ListView):
    model = Product
    template_name = 'catalog/home.html'
    context_object_name = 'products'
    paginate_by = 9

    def get_queryset(self):
        return get_products_from_cache()


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Каталог товаров'
        context['categories'] = get_categories_from_cache()
        return context


class ContactsTemplateView(TemplateView):
    template_name = 'catalog/contacts.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['contact'] = Contact.objects.first()
        context['title'] = 'Контакты'
        return context


class ProductDetailView(DetailView):
    model = Product
    template_name = 'catalog/product_detail.html'
    context_object_name = 'product'


class ProductCreateView(LoginRequiredMixin, CreateView):
    model = Product
    fields = ('name', 'description', 'price', 'category', 'image', 'is_published')
    success_url = reverse_lazy('catalog:home')

    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super().form_valid(form)


class ProductUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Product
    success_url = reverse_lazy('catalog:home')

    def get_form_class(self):
        user = self.request.user

        if user.has_perm('catalog.can_unpublish_product'):
            self.fields = ('is_published',)

        elif user == self.get_object().owner:
            self.fields = ('name', 'description', 'price', 'category', 'image')

        return super().get_form_class()

    def test_func(self):
        product = self.get_object()
        user = self.request.user

        return user == product.owner or user.has_perm('catalog.can_unpublish_product')


class ProductDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Product
    template_name = 'catalog/product_confirm_delete.html'
    success_url = reverse_lazy('catalog:home')

    def test_func(self):
        product = self.get_object()
        user = self.request.user

        is_owner = user == product.owner
        is_moderator = user.has_perm('catalog.delete_product')
        return is_owner or is_moderator
