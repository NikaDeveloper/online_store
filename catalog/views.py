from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.shortcuts import render, redirect, get_object_or_404
from .models import Product, Contact, Category


def home(request):
    # 1. Получаем все продукты, отсортированные по дате создания
    product_list = Product.objects.all().order_by('-created_at')

    # 2. Создаем объект Paginator: 9 товаров на страницу
    paginator = Paginator(product_list, 9)

    # 3. Получаем номер текущей страницы из GET-параметра 'page'
    page = request.GET.get('page')

    try:
        # Получаем объекты для запрошенной страницы
        products = paginator.page(page)
    except PageNotAnInteger:
        # Если параметр 'page' не число, показываем первую страницу
        products = paginator.page(1)
    except EmptyPage:
        # Если страница выходит за пределы, показываем последнюю
        products = paginator.page(paginator.num_pages)

    context = {
        'title': 'Каталог товаров',
        'products': products,
    }
    return render(request, 'catalog/home.html', context)


def contacts(request):
    # Метод .first() получает первую запись из таблицы Contact.
    # Мы используем его, потому что у магазина обычно только один набор контактов.
    contact_data = Contact.objects.first()

    context = {
        'title': 'Контакты Skystore',
        'contact': contact_data  # Передаем объект контакта в шаблон
    }
    return render(request, 'catalog/contacts.html', context)


def product_detail(request, pk):
    product = get_object_or_404(Product, pk=pk)

    context = {
        'title': product.name,
        'product': product
    }
    return render(request, 'catalog/product_detail.html', context)


def create_product(request):
    # Если пользователь отправляет форму (POST-запрос)
    if request.method == 'POST':
        # 1. Получаем данные из формы
        name = request.POST.get('name')
        description = request.POST.get('description')
        price = request.POST.get('price')
        category_id = request.POST.get('category')
        # Изображение получаем через request.FILES
        image = request.FILES.get('image')

        # 2. Находим объект категории (важно для ForeignKey)
        try:
            category = Category.objects.get(pk=category_id)
        except Category.DoesNotExist:
            # Обработка ошибки, если категория не найдена
            category = None

            # 3. Создаем и сохраняем новый продукт
        if category and name and price:
            Product.objects.create(
                name=name,
                description=description,
                price=price,
                category=category,
                image=image  # Django сам обработает загрузку файла
            )
            # Перенаправляем пользователя на главную страницу после успешного сохранения
            return redirect('catalog:home')

            # Если пользователь просто открывает страницу (GET-запрос)
    # Передаем все категории в шаблон, чтобы пользователь мог выбрать одну
    categories = Category.objects.all()

    context = {
        'title': 'Добавить товар',
        'categories': categories,
    }
    return render(request, 'catalog/create_product.html', context)
