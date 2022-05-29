from django.views.generic import ListView, DetailView, CreateView, DeleteView, UpdateView, View
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.utils.decorators import method_decorator
from django.contrib.auth.models import Group


from .filters import PostFilter
from .forms import PostForm, CommentForm
from .models import Post, Author, Category, Comment, Common


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
        return context

    def form_valid(self, form, *args, **kwargs):
        user = self.request.user
        common = Common.objects.get(user=user)
        form.instance.common = common
        form.instance.post = self.get_object()
        return super(PostDetailView, self).form_valid(form)


@method_decorator(login_required, name='dispatch')
class PostSearchView( ListView):

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
