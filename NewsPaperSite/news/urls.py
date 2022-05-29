from django.urls import path

from .views import *


urlpatterns = [
    path('', PostListView.as_view(), name='all_post'),
    path('<int:pk>', PostDetailView.as_view(), name='post'),
    path('create/', PostCreateView.as_view(), name='post_create'),
    path('<int:pk>/delete', PostDeleteView.as_view(), name='post_delete'),
    path('search/', PostSearchView.as_view(), name='post_search'),
    path('<int:pk>/update', PostUpdateView.as_view(), name='post_update'),
    path('upgrade/', upgrade_me, name='upgrade'),
    path('<int:pk>/category', CategoryPostView.as_view(), name='category_post'),
]
