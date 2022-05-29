from django.shortcuts import render
from django.views.generic import ListView
from news.models import Author, Post


class AuthorsPostListView(ListView):
    model = Post
    template_name = 'by_authors.html'
    context_object_name = 'all_post'
    ordering = ['-data_time']
    paginate_by = 3

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        author = Author.objects.get(user=self.request.user)
        context['all_authors_post'] = Post.objects.filter(author=author)
