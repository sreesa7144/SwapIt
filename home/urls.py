from django.urls import path
from . import views
from . models import FavBooks
from django.conf import settings
from django.conf.urls.static import static
app_name='home'
urlpatterns=[
    path('',views.HomeView,name='home'),
    path('addBooks/',views.addBooks,name='addBooks'),
    path('uploadpic/',views.uploadPic,name='uploadPic'),
    path('myBooks/',views.BooksView.as_view(),name='myBooks'),
    path('<int:pk>/', views.BookDetailsView.as_view(), name='myBooks'),
    path('<int:pk>/userbooks/', views.UsersBooksView, name='userBooks'),
    path('search/', views.SearchedBooks, name='searchedBooks'),
    path('favoriteAjax/', views.favorite_ajax, name='favoriteAjax'),
    path('removefavoriteAjax/', views.removefavorite_ajax, name='removefavoriteAjax'),
    path('wishList/',views.WishlistView.as_view(),name='wishList'),
    path('deletebook/', views.deleteBook, name='deleteBook'),
    ]