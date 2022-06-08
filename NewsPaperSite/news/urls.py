from django.urls import path, include

from .views import *


urlpatterns = [
    path('news/', include([
        path('', PostListView.as_view(), name='all_post'),
        path('<int:pk>', PostDetailView.as_view(), name='post'),
        path('create/', PostCreateView.as_view(), name='post_create'),
        path('<int:pk>/delete', PostDeleteView.as_view(), name='post_delete'),
        path('search/', PostSearchView.as_view(), name='post_search'),
        path('<int:pk>/update', PostUpdateView.as_view(), name='post_update'),
        path('upgrade/', upgrade_me, name='upgrade'),
        path('<int:pk>/category', CategoryPostView.as_view(), name='category_post')
    ])),
    path('profile/<str:slug>/', include([
        path('', ProfileView.as_view(), name='profile'),
        path('comment/', CommonCommentsView.as_view(),name='profile_comment_post'),
        # path('favorite', ProfileFavoritePost.as_view(), name='profile_favorite_post'),
        # path('edit', ProfileEditView.as_view(), name='profile_edit')
    ]))
]