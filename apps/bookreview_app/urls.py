from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$',views.index),
    url(r'login$',views.login),
    url(r'register$',views.register),
    url(r'logout$',views.logout),
    url(r'books$',views.homepage),
    url(r'add_book$',views.add_book),
    url(r'add_book_review$',views.add_book_review),
    url(r'books/(?P<book_id>\d+)$',views.view_book),
    url(r'users/(?P<user_id>\d+)$',views.view_user),
    url(r'delete/(?P<review_id>\d+)$',views.delete_review),
    url(r'add_review$',views.add_review)
]