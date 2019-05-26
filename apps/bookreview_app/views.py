from django.shortcuts import render, redirect
from django.contrib import messages
from .models import User, Book, Review, Author
import bcrypt

# Create your views here.
def index(request):
    return render(request,'bookreview_app/login_reg.html')

def register(request):
    reg_errors = User.objects.reg_validator(request.POST)
    if len(reg_errors) > 0:
        for key,value in reg_errors.items():
            messages.error(request, value, extra_tags=key)
        return redirect(index)
    user = User.objects.create(fname=request.POST['fname'],lname=request.POST['lname'],birthday=request.POST['birthday'],email=request.POST['email_r'],password=bcrypt.hashpw(request.POST['password_r'].encode(), bcrypt.gensalt()))
    request.session['fname']=request.POST['fname']
    request.session['user_id']=user.id
    return redirect('/books')

def login(request):
    login_errors = User.objects.login_validator(request.POST)
    if len(login_errors) > 0:
        for key,value in login_errors.items():
            messages.error(request, value, extra_tags=key)
        return redirect(index)

    user = User.objects.filter(email=request.POST['email']).values()
    for e in user:
        request.session['fname']=e['fname']
        request.session['user_id']=e['id']
    return redirect('/books')

def homepage(request):
    if 'fname' in request.session:
        books_to_exclude = [o.book.id for o in Review.objects.all().order_by('-created_at')[:3]]
        context = {
            "name": request.session['fname'],
            "books": Book.objects.all().exclude(id__in=books_to_exclude),
            "reviews": Review.objects.all().order_by('-created_at')[:3],
        }
        return render(request,'bookreview_app/books.html',context)
    return redirect('/')

def add_book(request):
    if 'fname' in request.session:
        context = {
            "authors": Author.objects.all()
        }
        return render(request,'bookreview_app/add_book.html',context)
    return redirect('/')

def add_book_review(request):
    if 'fname' in request.session:
        user = User.objects.get(id=request.session['user_id'])
        if request.POST['new_author']:
            print("*"*50,"new_author")
            author = Author.objects.create(name=request.POST['new_author'])
        else:
            print("*"*50,"list author")
            author = Author.objects.get(name=request.POST['author'])
        book = Book.objects.create(title=request.POST['title'],author=author)
        Review.objects.create(user=user,book=book,rating=request.POST['rating'],content=request.POST['content'])
        return redirect(view_book, book.id)
    return redirect('/')

def view_book(request, book_id):
    if 'fname' in request.session:
        request.session['book_id'] = book_id
        context = {
            "user_id": request.session['user_id'],
            "book": Book.objects.get(id=book_id),
            "reviews": Review.objects.filter(book=Book.objects.get(id=book_id))
        }
        return render(request,'bookreview_app/view_book.html',context)
    return redirect('/')

def view_user(request, user_id):
    if 'fname' in request.session:
        context = {
            "user": User.objects.get(id=user_id),
            "count": Review.objects.filter(user=User.objects.get(id=user_id)).count(),
            "reviews": Review.objects.filter(user=User.objects.get(id=user_id))
        }
        return render(request,'bookreview_app/view_user.html',context)
    return redirect('/')

def add_review(request):
    if 'fname' in request.session:
        user = User.objects.get(id=request.session['user_id'])
        book = Book.objects.get(id=request.session['book_id'])
        Review.objects.create(user=user,book=book,rating=request.POST['rating'],content=request.POST['content'])
        return redirect(view_book,request.session['book_id'])
    return redirect('/')

def delete_review(request,review_id):
    if 'fname' in request.session:
        review = Review.objects.get(id=review_id)
        review.delete()
        return redirect(view_book,request.session['book_id'])
    return redirect('/')

def logout(request):
    request.session.clear()
    return redirect('/')