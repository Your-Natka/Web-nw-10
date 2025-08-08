# pylint: disable=no-member
from django.urls import path
from . import views

urlpatterns = [
    path('', views.main_view, name='home'),
    path('signup/', views.signup, name='signup'),  # 🔧 виправлено
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('add/', views.add_quote, name='add_quote'),
    path('author/<int:author_id>/', views.author_detail, name='author_detail'),
    path('tag/<str:tag_name>/', views.quotes_by_tag, name='quotes_by_tag'),
    path('top-tags/', views.top_tags, name='top_tags'),
]