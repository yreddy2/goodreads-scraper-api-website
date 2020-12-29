# This file connects the url to the method that renders the pages
from django.contrib import admin

from django.urls import path

from . import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('home/', views.home),
    path('books/', views.books),
    path('book/<str:_id>/', views.book_detailed, name="book"),
    path('update/book/', views.book_update),
    path('add/book/form', views.add_book_form),
    path('add/book', views.add_book),
    path('delete/book/<str:_id>/', views.delete_book, name="delete_book"),
    path('authors/', views.authors),
    path('author/<str:_id>/', views.author_detailed, name="author"),
    path('update/author/', views.author_update),
    path('add/author/form', views.add_author_form),
    path('delete/author/<str:_id>/', views.delete_author, name="delete_author"),
    path('query/most-book-authors/', views.query1),
    path('vis/rank-authors/', views.vis1),
    path('vis/rank-books/', views.vis2),
]
