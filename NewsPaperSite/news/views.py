from django.http import HttpResponse
from django.views.generic import ListView, DetailView, CreateView, DeleteView, UpdateView, View
from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.utils.decorators import method_decorator
from django.contrib.auth.models import Group
from requests import request

from .filters import PostFilter
from .forms import PostForm, CommentForm
from .models import Post, Author, Category, Comment, Common, FavoritesPost


class PostListView(ListView):

    model = Post
    template_name = 'home.html'
    context_object_name = 'all_post'
    ordering = ['-data_time']
    paginate_by = 3

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['is_not_authors'] = not self.request.user.groups.filter(name='authors').exists()
        context['all_category'] = Category.objects.all()
        return context


@login_required
def upgrade_me(request):

    user = request.user
    authors_group = Group.objects.get(name='authors')

    if not request.user.groups.filter(name='authors').exists():
        authors_group.user_set.add(user)
        Author.objects.create(user=user)
    return redirect('/news/')

class PostCreateView(PermissionRequiredMixin, CreateView):

    template_name = 'post_create.html'
    form_class = PostForm
    success_url = '/account/login/'
    permission_required = ('news.add_post')

    def form_valid(self, form):
        user = self.request.user
        author = Author.objects.get(user=user)
        form.instance.author = author
        return super(PostCreateView, self).form_valid(form)


class PostDeleteView(PermissionRequiredMixin, DeleteView):

    template_name = 'post_delete.html'
    queryset = Post.objects.all()
    success_url = '/account/login/'
    permission_required = ('news.delete_post')



class PostUpdateView(PermissionRequiredMixin, UpdateView):

    template_name = 'post_update.html'
    form_class = PostForm
    success_url = '/account/login/'
    permission_required = ('news.change_post')

    def get_object(self,**kwargs):
        id = self.kwargs.get('pk')
        return Post.objects.get(pk=id)


class PostDetailView(DetailView, CreateView):

    model = Post
    template_name = 'flatpages/post.html'
    context_object_name = 'post'
    form_class = CommentForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['all_posts'] = Post.objects.filter(author=self.object.author)
        context['all_category'] = Category.objects.all()
        context['all_comment_post'] = Comment.objects.filter(post=self.object)
        common = Common.objects.get(user=self.request.user)
        context['not_in_favorite'] = not FavoritesPost.objects.filter(common=common, post=self.object).exists()
        return context

    def form_valid(self, form, *args, **kwargs):
        user = self.request.user
        common = Common.objects.get(user=user)
        form.instance.common = common
        form.instance.post = self.get_object()
        return super(PostDetailView, self).form_valid(form)

    def post(self, request, *args, **kwargs):

        self.object = self.get_object()
        context = self.get_context_data()
        common = Common.objects.get(user=self.request.user)

        if request.POST.get("add_favorite") and "add_favorite":
            common = Common.objects.get(user=self.request.user)
            FavoritesPost.objects.create(common=common, post=self.object)

        elif request.POST.get("delete_favorite") and "delete_favorite":
            common = Common.objects.get(user=self.request.user)
            FavoritesPost.objects.get(common=common, post=self.object).delete()

        elif request.POST.get("add_comment"):
            form = CommentForm(self.request.POST)
            form.instance.common = common
            form.instance.post = self.get_object()
            return super(PostDetailView, self).form_valid(form)

        return render(request, "flatpages/post.html", context=context)

@method_decorator(login_required, name='dispatch')
class PostSearchView(ListView):

    model = Post
    template_name = 'post_search.html'
    context_object_name = 'filter_post'
    ordering = ['-data_time']

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filter'] = PostFilter(self.request.GET, queryset=self.get_queryset())
        return context


class CategoryPostView(DetailView):

    model = Category
    template_name = 'post_category.html'
    context_object_name = 'category'

    def get_context_data(self,  **kwargs):
        context = super().get_context_data(**kwargs)
        context['all_posts'] = Post.objects.filter(category=self.object)
        return context


class ProfileView(DetailView):

    model = Common
    template_name = 'profile/profile_post.html'
    context_object_name = 'common'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        if Author.objects.filter(user=self.object.user).exists():
            author = Author.objects.get(user=self.object.user)
            context['author'] = author
            context['no_post'] = not Post.objects.filter(author=author).exists()

            if Post.objects.filter(author=author).exists():
                context['author_posts'] = Post.objects.filter(author=author).order_by('-data_time')

        context['is_not_authors'] = not self.request.user.groups.filter(name='authors').exists()
        context['is_author'] = self.request.user.groups.filter(name='authors').exists()
        context['popular_posts'] = Post.objects.all()
        return context

class CommonCommentsView(DetailView):

    model = Common
    template_name = 'profile/common_comments.html'
    context_object_name = 'common'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        if Author.objects.filter(user=self.object.user).exists():
            author = Author.objects.get(user=self.object.user)
            context['author'] = author

        if Comment.objects.filter(common=self.object).exists():
            context['common_comments'] = Comment.objects.filter(common=self.object)

        context['is_not_authors'] = not self.request.user.groups.filter(name='authors').exists()
        context['is_author'] = self.request.user.groups.filter(name='authors').exists()
        context['no_comments'] = not Comment.objects.filter(common=self.object).exists()
        context['popular_posts'] = Post.objects.all()
        return context

class ProfileFavoritePostView(DetailView):

    model = Common
    template_name = 'profile/favorite_posts.html'
    context_object_name = 'common'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        if Author.objects.filter(user=self.object.user).exists():
            author = Author.objects.get(user=self.object.user)
            context['author'] = author

        context['is_not_authors'] = not self.request.user.groups.filter(name='authors').exists()
        context['is_author'] = self.request.user.groups.filter(name='authors').exists()
        context['no_comments'] = not Comment.objects.filter(common=self.object).exists()
        context['popular_posts'] = Post.objects.all()
        return context