from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy, reverse
from django.core.mail import send_mail
from django.conf import settings
from .models import BlogEntry


class BlogEntryCreateView(CreateView):
    model = BlogEntry
    fields = ('title', 'content', 'preview', 'is_published')
    template_name = 'blog/blogentry_form.html'
    success_url = reverse_lazy('blog:list')


class BlogEntryListView(ListView):
    model = BlogEntry
    template_name = 'blog/blogentry_list.html'
    context_object_name = 'blog_entries'

    def get_queryset(self, *args, **kwargs):
        queryset = super().get_queryset(*args, **kwargs)
        queryset = queryset.filter(is_published=True)
        return queryset


class BlogEntryDetailView(DetailView):
    model = BlogEntry
    template_name = 'blog/blogentry_detail.html'
    context_object_name = 'blog_entry'
    slug_field = 'slug'

    def get_object(self, queryset=None):
        self.object = super().get_object(queryset)
        self.object.views_count += 1
        self.object.save()

        if self.object.views_count == 100:
            send_mail(
                subject='Поздравляем с 100 просмотрами!',
                message=f'Ваша статья "{self.object.title}" набрала 100 просмотров.',
                from_email=settings.EMAIL_HOST_USER,
                recipient_list=[settings.EMAIL_FOR_NOTIFICATIONS],
                fail_silently=False,
            )

        return self.object


class BlogEntryUpdateView(UpdateView):
    model = BlogEntry
    fields = ('title', 'content', 'preview', 'is_published')
    template_name = 'blog/blogentry_form.html'
    slug_field = 'slug'

    def get_success_url(self):
        # Используем reverse с аргументом, чтобы перенаправить на страницу статьи
        return reverse('blog:view', kwargs={'slug': self.object.slug})


class BlogEntryDeleteView(DeleteView):
    model = BlogEntry
    template_name = 'blog/blogentry_confirm_delete.html'
    success_url = reverse_lazy('blog:list')
