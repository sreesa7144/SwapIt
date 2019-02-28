from django.db import models
from django.contrib.auth.models import User
class UserBooks(models.Model):
    user_id = models.ForeignKey(User,on_delete=models.CASCADE,null=True)
    username = models.CharField(max_length=200)
    book_name = models.CharField(max_length=200)
    book_author = models.CharField(max_length=200)
    book_ISBN=models.CharField(max_length=200)
    book_genre = models.CharField(max_length=200)
    book_status=models.BooleanField(default=False)
    book_url=models.URLField(max_length=128)
    book_rating = models.IntegerField(default=0)
    def __str__(self):
        return self.book_name
class FavBooks(models.Model):
    user_id = models.ForeignKey(User,on_delete=models.CASCADE,null=True)
    book_id= models.ForeignKey(UserBooks,on_delete=models.CASCADE,null=True)
    class Meta:
        unique_together = (("user_id", "book_id"),)


class BooksIsbn(models.Model):
    book_ISBN = models.CharField(max_length=100,unique=True)
    count = models.IntegerField()

class Images(models.Model):
    user_id=models.ForeignKey(User,on_delete=models.CASCADE,null=True)
    image=models.FileField()
