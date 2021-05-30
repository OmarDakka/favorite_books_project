from books_app.models import Book, add_fav_book, create_book, delete_user_book, get_fav_books, remove_fav_book
from django.shortcuts import redirect, render
from login_app.models import users
from django.contrib import messages



def homepage(request):
    user = request.session['first_name'] + " " + request.session['last_name']
    user_id = request.session['id']
    all_books = Book.objects.all()
    fav_books = get_fav_books(request.session['id'])
    context = {
        "user" : user,
        "user_id" : user_id,
        "all_books" : all_books,
        "fav_books" : fav_books
    }
    return render(request,'books.html', context)

def add_book(request):
    errors = Book.objects.form_validator(request.POST)
    if len(errors) > 0:
                for key, value in errors.items():
                    messages.error(request, value)
                return redirect("/books")
    else : 
        create_book(request.POST["bookTitle"],request.POST['description'],users.objects.get(id = request.session['id']))
    return redirect("/books")

def add_fav(request,book_id):
    if "id" in request.session:
        add_fav_book(request.session['id'],book_id)
        return redirect("/books")
    
def view_book(request,book_id):
    user = request.session['first_name'] + " " + request.session['last_name']
    user_id = request.session['id']
    current_book = Book.objects.get(id = book_id)
    fav_books = get_fav_books(request.session['id'])
    users_who_liked = current_book.users_who_like.all()
    current_user_like = current_book.users_who_like.filter(id = user_id).count() < 1
    context = {
        "user" : user,
        "user_id" : user_id,
        "fav_books" : fav_books,
        "current_book" : current_book,
        "users_who_liked" : users_who_liked,
        "current_user_like" : current_user_like
    }
    return render(request,"view_book.html",context)

def delete_book(request,book_id):
    delete_user_book(book_id)
    return redirect("/books")

def update_book(request,book_id):
    if request.method == "POST":
        this_show = Book.objects.get(id = book_id)
        this_show.title = request.POST['bookName']
        this_show.description = request.POST['desc']
        this_show.save()
        return redirect(f"/books/{book_id}")

def remove_book(request,book_id):
    remove_fav_book(request.session['id'],book_id)
    return redirect(f"/books/{book_id}")

def add_fav_views(request,book_id):
    if "id" in request.session:
        add_fav_book(request.session['id'],book_id)
        return redirect(f"/books/{book_id}")
