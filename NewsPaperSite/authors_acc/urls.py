from django.urls import path
from .views import AuthorsPostListView


urlpatterns = [
    path('', AuthorsPostListView.as_view(), name='by_authors')
]
