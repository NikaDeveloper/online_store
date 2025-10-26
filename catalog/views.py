from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import ListView, TemplateView, DetailView, CreateView, UpdateView, DeleteView
from .models import Product, Contact
from django.urls import reverse_lazy, reverse
from .forms import ProductForm


class ProductListView(ListView):
    model = Product
    template_name = 'catalog/home.html'
    context_object_name = 'products'
    paginate_by = 9


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Каталог товаров'
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
