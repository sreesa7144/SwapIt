from django.contrib import admin
from . models import UserBooks,FavBooks,BooksIsbn,Images
admin.site.register(UserBooks)
admin.site.register(FavBooks)
admin.site.register(BooksIsbn)
admin.site.register(Images)
# Register your models here.
