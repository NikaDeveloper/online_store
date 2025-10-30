from catalog.models import Product, Category
from config.settings import CACHE_ENABLED
from django.core.cache import cache


def get_products_from_cache():
    """ Получает данные по продуктам из кэша, если кэш пуст, получает данные из БД"""
    if not CACHE_ENABLED:
        return Product.objects.all()
    key = 'products_list'
    products = cache.get(key)
    if products is not None:
        return products
    products = Product.objects.all()
    cache.set(key, products)
    return products


def get_products_by_category_from_cache(category_pk):
    """ Получает список продуктов по категории из кэша, или из БД """
    if not CACHE_ENABLED:
        return Product.objects.filter(category_id=category_pk)

    # Уникальный ключ для кеша, зависящий от ID категории
    key = f'products_by_category_{category_pk}'
    products = cache.get(key)

    if products is not None:
        return products

    # Если в кеше нет, получаем из БД
    try:
        products = Product.objects.filter(category_id=category_pk)
        # Кешируем на 15 минут (60 * 15 секунд)
        cache.set(key, products, 60 * 15)
        return products
    except Exception:
        # Можно вернуть пустой список, если категория не найдена или ошибка
        return Product.objects.none()


def get_categories_from_cache():
    """ Получает список категорий из кэша, если кэш пуст, получает из БД """
    if not CACHE_ENABLED:
        return Category.objects.all()

    key = 'categories_list'
    categories = cache.get(key)

    if categories is not None:
        return categories

    categories = Category.objects.all()
    cache.set(key, categories, 60 * 60)
    return categories
