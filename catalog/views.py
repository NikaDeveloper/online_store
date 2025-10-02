from django.shortcuts import render
from .models import Product, Contact


def home(request):
    latest_products = Product.objects.all().order_by('-created_at')[:5]

    print("\n--- Последние 5 продуктов (консоль сервера) ---")
    for product in latest_products:
        print(f"ID: {product.id}, Название: {product.name}, Цена: {product.price}")
    print("-------------------------------------------------")

    context = {
        'title': 'Skystore: Главная страница',
        'latest_products': latest_products
    }
    return render(request, 'home.html', context)


def contacts(request):
    # Метод .first() получает первую запись из таблицы Contact.
    # Мы используем его, потому что у магазина обычно только один набор контактов.
    contact_data = Contact.objects.first()

    context = {
        'title': 'Контакты Skystore',
        'contact': contact_data  # Передаем объект контакта в шаблон
    }
    return render(request, 'contacts.html', context)
