"""
Definition of views.
"""

from datetime import datetime
from django.shortcuts import render, redirect
from django.http import HttpRequest
from .forms import AnketaForm
from .forms import PoolForm
from django.contrib.auth.forms import UserCreationForm

from django.db import models
from .models import Blog
from .forms import BlogForm

from .models import Comment
from .forms import CommentForm

def home(request):
    """Renders the home page."""
    assert isinstance(request, HttpRequest)
    return render(
        request,
        'app/index.html',
        {
            'title':'Домашняя страница',
            'year':datetime.now().year,
        }
    )

def contact(request):
    """Renders the contact page."""
    assert isinstance(request, HttpRequest)
    return render(
        request,
        'app/contact.html',
        {
            'title':'Контакт',
            'message':'Твоя контактная страница.',
            'year':datetime.now().year,
        }
    )

def about(request):
    """Renders the about page."""
    assert isinstance(request, HttpRequest)
    return render(
        request,
        'app/about.html',
        {
            'title':'О',
            'message':'Страница описания вашего приложения.',
            'year':datetime.now().year,
        }
    )
def source(request):
    """Renders the home page."""
    assert isinstance(request, HttpRequest)
    return render(
        request,
        'app/source.html',
        {
            'title':'Источники',
            'message':'Ссылки на источники',
            'year':datetime.now().year,
        }
    )
def anketa(request):
    assert isinstance(request,HttpRequest)
    data = None
    gender = {'1':'Мужчина','2':'Женщина'}
    internet = {'1':'Каждый день','2':'Несколько раз в день','3':'Несколько раз в неделю','4':'Несколько раз в месяц'}
    if request.method == 'POST':
        form = AnketaForm(request.POST)
        if form.is_valid():
            data = dict()
            data['name'] = form.cleaned_data['name']
            data['city'] = form.cleaned_data['city']
            data['job'] = form.cleaned_data['job']
            data['gender'] = form.cleaned_data['gender']
            data['internet'] = form.cleaned_data['internet']
            if (form.cleaned_data['notice'] == True):
                data['notice'] = 'Да'
            else:
                data['notice'] = 'Нет'
            data['email'] = form.cleaned_data['email']
            data['message'] = form.cleaned_data['message']
            form = None
    else:
        form = AnketaForm()
    return render(
                request,
                'app/anketa.html',
                {
                    'form':form,
                    'data':data
                }
            )
def pool(request):
    assert isinstance(request,HttpRequest)
    data = None
    gender = {'1':'Да','2':'Нет'}
    internet = {'1':'Отлично','2':'Хорошо','3':'Сносно','4':'Плохо'}
    if request.method == 'POST':
        form = PoolForm(request.POST)
        if form.is_valid():
            data = dict()
            data['name'] = form.cleaned_data['name']
            data['product'] = form.cleaned_data['product']
            data['score'] = form.cleaned_data['score']
            if (form.cleaned_data['notice'] == True):
                data['notice'] = 'Да'
            else:
                data['notice'] = 'Нет'
            data['email'] = form.cleaned_data['email']
            data['message'] = form.cleaned_data['message']
            form = None
    else:
        form = PoolForm()
    return render(
                request,
                'app/pool.html',
                {
                    'form':form,
                    'data':data
                }
            )
def registration(request):
    """Renders the registration."""

    if request.method == "POST":
        regform = UserCreationForm(request.POST)
        if regform.is_valid():
            reg_f = regform.save(commit=False)
            reg_f.is_staff = False
            reg_f.is_active = True
            reg_f.is_superuser = False
            reg_f.date_joined = datetime.now()
            reg_f.last_login = datetime.now()

            regform.save()

            return redirect('home')
    else:
        regform = UserCreationForm()

    assert isinstance(request,HttpRequest)
    return render(
                request,
                'app/registration.html',
                {
                    'regform': regform,
                    'year':datetime.now().year,
                }
            )
def blog(request):
    """Renders the registration."""
    posts = Blog.objects.all()
    assert isinstance(request, HttpRequest)
    return render(
        request,
        'app/blog.html',
        {
            'title':'Блог',
            'posts':posts,
            'year':datetime.now().year,
        }
    )
def blogpost(request,parametr):
    """Renders the registration."""
    
    assert isinstance(request, HttpRequest)
    post_1 = Blog.objects.get(id=parametr)
    comments=Comment.objects.filter(post=parametr)

    if request.method=="POST":
        form = CommentForm(request.POST)
        if form.is_valid():
            comment_f=form.save(commit=False)
            comment_f.author=request.user
            comment_f.date=datetime.now()
            comment_f.post=Blog.objects.get(id=parametr)
            comment_f.save()
            return redirect('blogpost',parametr=post_1.id)
    else:
        form=CommentForm()

    return render(
        request,
        'app/blogpost.html',
        {
            'post_1':post_1,

            'year':datetime.now().year,
            'comments':comments,

            'form':form,
        }
    )
def newpost(request):

    assert isinstance(request,HttpRequest)
    if request.method == "POST":
        blogform = BlogForm(request.POST, request.FILES)
        if blogform.is_valid():
            blog_f = blogform.save(commit=False)
            blog_f.posted = datetime.now()
            blog_f.autor = request.user
            blog_f.save()

            return redirect('blog')
    else:
        blogform = BlogForm()

    return render(
        request,
        'app/newpost.html',
        {
            'blogform': blogform,
            'title': 'Добавить статью блога',
            'year':datetime.now().year,
        }

    )
def videopost(request):
    """Renders the about page."""
    assert isinstance(request, HttpRequest)
    return render(
        request,
        'app/videopost.html',
        {
            'title':'Видео',
            'year':datetime.now().year,
        }
    )


