from django.contrib import auth
from django.db.models import Q
from django.shortcuts import render
from django.contrib.auth.models import User
from django.contrib.auth.context_processors import auth as AUTH
from .models import Category, Movie, Rating, Favorites

from .forms import Categoryform,Movieform,Userform

def home(request):
    return render(request,'index.html')

def register(request):
    if request.user.is_authenticated:
        auth.logout(request)
    regsuccess=False
    msg=''
    uname=''
    if request.method=='POST':
        uname = request.POST["username"]
        fname = request.POST["fname"]
        lname = request.POST["lname"]
        email = request.POST["email"]
        pwd1 = request.POST["password1"]
        pwd2 = request.POST["password2"]
        if User.objects.filter(username=uname).exists():
            msg=f'Username {uname} is already taken. use another Username'
            print(msg)
            return render(request, 'register.html', {'msg': msg, 'regsuccess': regsuccess, 'uname': uname})
        elif User.objects.filter(email=email).exists():
            msg=f'Email {email} is already taken. use another email'
            print(msg)
            return render(request, 'register.html', {'msg': msg, 'regsuccess': regsuccess, 'uname': uname})
        elif pwd1 != pwd2:
            msg = 'Passwords not matching'
            print(msg)
            return render(request, 'register.html', {'msg': msg, 'regsuccess': regsuccess, 'uname': uname})
        else:
            user=User.objects.create_user(username=uname,first_name=fname,last_name=lname,email=email,password=pwd1)
            user.save()
            msg=f'User {uname} registered successfully'
            print(msg)
            regsuccess=True
            return render(request,'login.html',{'msg':msg,'regsuccess':regsuccess,'uname':uname})
    return render(request,'register.html',{'msg':msg,'regsuccess':regsuccess,'uname':uname})

def login(request):
    loginsuccess,msg,uname=False,'',''
    if request.method=='POST':
        uname=request.POST['uname']
        pwd=request.POST['pwd']
        user=auth.authenticate(username=uname,password=pwd)
        if user is not None:
            auth.login(request,user)
            msg=f'User {uname} logged in successfully'
            loginsuccess=True
            print(msg)
            return render(request,'index.html',{'msg':msg,'loginsuccess':loginsuccess,'uname':uname})
        else:
            msg='invalid username or password'
            print(msg)
            return render(request,'login.html',{'msg':msg,'loginsuccess':loginsuccess,'uname':uname})
    return render(request, 'login.html', {'msg': msg, 'loginsuccess': loginsuccess, 'uname': uname})


def logout(request):
    logoutsuccess=True
    auth.logout(request)
    msg='logged out successfully'
    print(msg)
    return render(request, 'index.html', {'msg': msg, 'logoutsuccess': logoutsuccess})


def addamovie(request):
    categories=Category.objects.all()
    msg=''
    if request.method == 'POST':
        name = request.POST.get('name')
        desc = request.POST.get('desc')
        pict = request.FILES.get('pict')
        actors = request.POST.get('actors')
        utubelink = request.POST.get('utubelink')
        category = Category.objects.get(name=request.POST.get('category'))
        released = request.POST.get('released')
        user = User.objects.get(username=request.user.username)
        movobject = Movie(name=name, desc=desc, pict=pict,user=user,actors=actors,utubelink=utubelink,category=category,released=released)
        movobject.save()
        msg=f"movie '{name}' added successfully"
    return render(request, 'addamovie.html',{'msg':msg,'categories':categories})

def addagenre(request):
    msg=''
    if request.method == 'POST':
        name = request.POST.get('name')
        desc = request.POST.get('desc')
        pict = request.FILES.get('pict')
        user = User.objects.get(username=request.user.username)
        catobject = Category(name=name, desc=desc, pict=pict,user=user)
        catobject.save()
        msg=f"movie category '{name}' added successfully"
    return render(request, 'addagenre.html',{'msg':msg})

def viewmodgenre(request,msg=''):
    categories=Category.objects.all().filter(user=request.user)
    return render(request, 'viewmodgenre.html',{'msg':msg,'categories':categories})
def delcat(request,catid):
    catobj=Category.objects.get(id=catid)
    name=catobj.name
    catobj.delete()
    msg = f"Category '{name}' deleted successfully"
    return viewmodgenre(request,msg=msg)
def modcat(request,catid):
    msg=''
    cat=Category.objects.get(id=catid)
    form=Categoryform(request.POST or None, request.FILES, instance=cat)
    if form.is_valid():
        name=cat.name
        form.save()
        msg = f"Category '{name}' modified successfully"
    return render(request, 'modcat.html',{'msg':msg,'form':form})
def viewmodmovie(request,msg=''):
    movies=Movie.objects.all().filter(user=request.user)
    return render(request, 'viewmodmovie.html',{'msg':msg,'movies':movies})
def delmov(request,movid):
    movobj=Movie.objects.get(id=movid)
    name=movobj.name
    movobj.delete()
    msg = f"Category '{name}' deleted successfully"
    return viewmodmovie(request,msg=msg)
def modmov(request,movid):
    msg=''
    mov=Movie.objects.get(id=movid)
    form=Movieform(request.POST or None, request.FILES, instance=mov)
    if form.is_valid():
        name=mov.name
        form.save()
        msg = f"Movie '{name}' modified successfully"
    return render(request, 'modmov.html',{'msg':msg,'form':form})

def viewmodprofile(request,msg=''):
    return render(request, 'viewmodprofile.html',{'msg':msg,'u':request.user})

def modprofile(request):
    msg=''
    pro=User.objects.get(username=request.user.username)
    form=Userform(request.POST or None, request.FILES, instance=pro)
    if form.is_valid():
        name=pro.username
        form.save()
        msg = f" '{name}' modified successfully"
    return render(request, 'modprofile.html',{'msg':msg,'form':form})
def chgpwd(request,msg=''):
    if request.method == 'POST':
        name=request.user.username
        u = User.objects.get(username=name)
        u.set_password(request.POST.get('password'))
        u.save()
        msg=f"Password for '{name}' changed successfully"
    return render(request, 'chgpwd.html',{'msg':msg})
def findmovies(request,msg=''):
    movies=None
    if 'q' in request.GET:
        query=request.GET.get('q')
        movies=Movie.objects.all().filter( Q(name__contains=query) | Q(desc__contains=query)| Q(actors__contains=query) )
        msg=f"Query '{query}' gave '{movies.count()}' results"
    return render(request,'findmovies.html',{'movies':movies,'msg':msg})
def ratenreview(request,movid,msg=''):
    m = Movie.objects.get(id=movid)
    if request.method == 'POST':
        review = request.POST.get('review')
        rating = int(request.POST.get('rating'))
        user = request.user
        ratobj_already=Rating.objects.all().filter(name=m,user=user)
        if ratobj_already:
            ratobj_already.review = review
            ratobj_already.rating = rating
            msg = f"Movie '{m.name}' rating/review updated successfully"
        else:
            ratobj=Rating(name=m,review=review,rating=rating,user=user)
            ratobj.save()
            msg=f"Movie '{m.name}' is rated/reviewed successfully"
    return render(request,'ratenreview.html',{'m':m,'msg':msg})
def addfav(request,movid):
    movie = Movie.objects.get(id=movid)
    user = request.user
    alreadyfav=Favorites.objects.all().filter(movie=movie,user=user)
    msg = f"Movie '{movie.name}' is already in ur favorites list"
    if not alreadyfav:
        favobj=Favorites(movie=movie,user=user)
        favobj.save()
        print('save')
        msg = f"Movie '{movie.name}' is added to ur favorites list"
    return findmovies(request,msg=msg)
def movcatwise(request):
    cat=Category.objects.all()
    catmov=dict()
    for c in cat:
        catmov[c]=Movie.objects.all().filter(category=c)
    return render(request, 'movcatwise.html', {'catmov': catmov})
def seerevrat(request,movid):
    movie = Movie.objects.get(id=movid)
    ratobj=Rating.objects.all().filter(name=movie)
    if ratobj:
        msg=f"Movie '{movie.name}' has following reviews"
    else:
        msg=f"Movie '{movie.name}' has no reviews yet"
    return render(request, 'seerevrat.html', {'msg': msg,'ratobj':ratobj})
def favs(request):
    favs=Favorites.objects.all().filter(user=request.user)
    if favs:
        msg='You have no movies in favorites list'
    else:
        msg="You have '{favs.count()}' movies in favorites list"
    return render(request, 'favs.html', {'msg': msg,'favs':favs})
