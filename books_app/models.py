from django.db import models
from django.db.models.deletion import CASCADE
from django.db.models.fields import DateTimeField
from login_app.models import users

# Create your models here.
class UserManager(models.Manager):
    def form_validator(self, postData):
        errors = {}
        if len(postData['bookTitle']) == 0:
            errors["bookTitle"] = "The book title is required!"
        if len(postData['description']) < 5:
            errors["description"] = "The description should be at least 5 characters!"
        return errors


class Book(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    uploaded_by = models.ForeignKey(users,related_name="books_uploaded", on_delete=CASCADE)
    users_who_like = models.ManyToManyField(users,related_name="liked_books")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = UserManager()


def create_book(text,description,users):
    created_book = Book.objects.create(title = text, description = description ,uploaded_by = users)
    users.liked_books.add(created_book)
    return created_book


def get_fav_books(user_id):
    user = users.objects.get(id = user_id)
    return user.liked_books.all()


def add_fav_book(user_id , book_id):
    user = users.objects.get(id = user_id)
    book = Book.objects.get(id = book_id)
    return user.liked_books.add(book)


def remove_fav_book(user_id, book_id):
    user = users.objects.get(id = user_id)
    book = Book.objects.get(id = book_id)
    return user.liked_books.remove(book)


def delete_user_book(book_id):
    book = Book.objects.get(id = book_id)
    return book.delete()