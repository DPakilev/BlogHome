from django.http import HttpResponse
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, DeleteView, UpdateView
from django.views.generic.edit import FormMixin
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
    paginate_by = 4

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['is_author'] = self.request.user.groups.filter(name='authors').exists()
        context['all_categories'] = Category.objects.all()
        context['popular_posts'] = Post.objects.order_by('-in_favorite')
        if self.request.user.is_authenticated:
            context['common'] = Common.objects.get(user=self.request.user)
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

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['is_author'] = self.request.user.groups.filter(name='authors').exists()
        context['all_categories'] = Category.objects.all()
        context['popular_posts'] = Post.objects.order_by('-in_favorite')
        if self.request.user.is_authenticated:
            context['common'] = Common.objects.get(user=self.request.user)
        return context

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

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['is_author'] = self.request.user.groups.filter(name='authors').exists()
        context['all_categories'] = Category.objects.all()
        context['popular_posts'] = Post.objects.order_by('-in_favorite')
        if self.request.user.is_authenticated:
            context['common'] = Common.objects.get(user=self.request.user)
        return context


class PostUpdateView(PermissionRequiredMixin, UpdateView):

    template_name = 'post_update.html'
    form_class = PostForm
    success_url = '/account/login/'
    permission_required = ('news.change_post')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['is_author'] = self.request.user.groups.filter(name='authors').exists()
        context['all_categories'] = Category.objects.all()
        context['popular_posts'] = Post.objects.order_by('-in_favorite')
        if self.request.user.is_authenticated:
            context['common'] = Common.objects.get(user=self.request.user)
        return context


    def get_object(self,**kwargs):
        id = self.kwargs.get('pk')
        return Post.objects.get(pk=id)


class PostDetailView(FormMixin, DetailView):

    model = Post
    template_name = 'post.html'
    context_object_name = 'post'
    form_class = CommentForm

    def get_success_url(self, **kwargs):
        return reverse_lazy('post', kwargs={'pk':self.get_object().id})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['is_author'] = self.request.user.groups.filter(name='authors').exists()
        context['all_posts'] = Post.objects.filter(author=self.object.author)
        context['all_category'] = Category.objects.all()
        context['all_comment_post'] = Comment.objects.filter(post=self.object)
        context['all_categories'] = Category.objects.all()
        context['popular_posts'] = Post.objects.order_by('-in_favorite')

        if self.request.user.is_authenticated:
            common = Common.objects.get(user=self.request.user)
            context['not_in_favorite'] = not FavoritesPost.objects.filter(common=common, post=self.object).exists()
            context['common'] = common
        return context

    def form_valid(self, form, *args, **kwargs):
        self.object = form.save(commit=False)
        self.object.post = self.get_object()
        self.object.common = Common.objects.get(user=self.request.user)
        self.object.save()
        return super().form_valid(form)

    def post(self, request, *args, **kwargs):

        self.object = self.get_object()
        if request.user.is_authenticated:
            if request.POST.get("add_favorite") and "add_favorite":
                common = Common.objects.get(user=self.request.user)
                FavoritesPost.objects.create(common=common, post=self.object)
                self.object.in_favorite += 1
                self.object.save()

            elif request.POST.get("delete_favorite") and "delete_favorite":
                common = Common.objects.get(user=self.request.user)
                FavoritesPost.objects.get(common=common, post=self.object).delete()
                self.object.in_favorite -= 1
                self.object.save()

            elif request.POST.get("add_comment"):
                form = self.get_form()
                if form.is_valid():
                    return self.form_valid(form)

        return redirect(self.get_success_url())

@method_decorator(login_required, name='dispatch')
class PostSearchView(ListView):

    model = Post
    template_name = 'post_search.html'
    context_object_name = 'filter_post'
    ordering = ['-data_time']

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['is_author'] = self.request.user.groups.filter(name='authors').exists()
        context['filter'] = PostFilter(self.request.GET, queryset=self.get_queryset())
        context['all_categories'] = Category.objects.all()
        context['popular_posts'] = Post.objects.order_by('-in_favorite')
        if self.request.user.is_authenticated:
            context['common'] = Common.objects.get(user=self.request.user)
        return context


class CategoryPostView(DetailView):

    model = Category
    template_name = 'post_category.html'
    context_object_name = 'category'

    def get_context_data(self,  **kwargs):
        context = super().get_context_data(**kwargs)
        context['is_author'] = self.request.user.groups.filter(name='authors').exists()
        context['all_posts'] = Post.objects.filter(category=self.object)
        context['all_categories'] = Category.objects.all()
        context['popular_posts'] = Post.objects.order_by('-in_favorite')
        if self.request.user.is_authenticated:
            context['common'] = Common.objects.get(user=self.request.user)
        return context


class ProfileView(DetailView):

    model = Common
    template_name = 'profile/profile_post.html'
    context_object_name = 'common'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        if self.request.user.is_authenticated:
            context['user_common'] = Common.objects.get(user=self.request.user)

        if Author.objects.filter(user=self.object.user).exists():
            author = Author.objects.get(user=self.object.user)
            context['no_post'] = not Post.objects.filter(author=author).exists()
            context['user_author'] = author

            if Post.objects.filter(author=author).exists():
                context['author_posts'] = Post.objects.filter(author=author).order_by('-data_time')

        if self.object.user.first_name == '':
            context['no_first_name'] = True

        if self.object.user.last_name == '':
            context['no_last_name'] = True

        if self.object.user == self.request.user:
            context['this_is_common'] = True

        context['all_categories'] = Category.objects.all()
        context['is_not_authors'] = not self.request.user.groups.filter(name='authors').exists()
        context['is_author'] = self.request.user.groups.filter(name='authors').exists()
        context['popular_posts'] = Post.objects.order_by('-in_favorite')
        return context

class CommonCommentsView(DetailView):

    model = Common
    template_name = 'profile/common_comments.html'
    context_object_name = 'common'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.user.is_authenticated:
            context['user_common'] = Common.objects.get(user=self.request.user)

        if Comment.objects.filter(common=self.object).exists():
            context['common_comments'] = Comment.objects.filter(common=self.object)

        if self.object.user.first_name == '':
            context['no_first_name'] = True

        if self.object.user.last_name == '':
            context['no_last_name'] = True

        if self.object.user == self.request.user:
            context['this_is_common'] = True

        context['all_categories'] = Category.objects.all()
        context['is_not_authors'] = not self.request.user.groups.filter(name='authors').exists()
        context['is_author'] = self.request.user.groups.filter(name='authors').exists()
        context['no_comments'] = not Comment.objects.filter(common=self.object).exists()
        context['popular_posts'] = Post.objects.order_by('-in_favorite')
        return context

class ProfileFavoritePostView(DetailView):

    model = Common
    template_name = 'profile/favorite_posts.html'
    context_object_name = 'common'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        if self.request.user.is_authenticated:
            context['user_common'] = Common.objects.get(user=self.request.user)

        if Author.objects.filter(user=self.object.user).exists():
            author = Author.objects.get(user=self.object.user)
            context['author'] = author

        if self.object.user.first_name == '':
            context['no_first_name'] = True

        if self.object.user.last_name == '':
            context['no_last_name'] = True

        if self.object.user == self.request.user:
            context['this_is_common'] = True

        context['favorite_posts'] = FavoritesPost.objects.filter(common=self.object)
        context['no_favorite_posts'] = not FavoritesPost.objects.filter(common=self.object).exists()
        context['is_not_authors'] = not self.request.user.groups.filter(name='authors').exists()
        context['is_author'] = self.request.user.groups.filter(name='authors').exists()
        context['no_comments'] = not Comment.objects.filter(common=self.object).exists()
        context['popular_posts'] = Post.objects.order_by('-in_favorite')
        context['all_categories'] = Category.objects.all()
        return context