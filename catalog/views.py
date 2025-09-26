from django.shortcuts import render

def home(request):
    return render(request, 'home.html')


def contacts(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        phone = request.POST.get('phone')
        message = request.POST.get('message')

        print(f'Пользователь {name}, Телефон: {phone}, Сообщение: {message}')

        context = {'success_message': 'Ваше сообщение успешно отправлено!'}
        return render(request, 'contacts.html', context)

    return render(request, 'contacts.html')

