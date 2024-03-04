from django.urls import path
from . import views
app_name='moviedb'
urlpatterns = [
    path('', views.home, name='home'),
    path('register/', views.register, name='register'),
    path('login/', views.login, name='login'),
    path('logout/', views.logout, name='logout'),
    path('addamovie/', views.addamovie, name='addamovie'),
    path('addagenre/', views.addagenre, name='addagenre'),
    path('viewmodgenre/', views.viewmodgenre, name='viewmodgenre'),
    path('viewmodmovie/', views.viewmodmovie, name='viewmodmovie'),
    path('delcat/<int:catid>/', views.delcat, name='delcat'),
    path('modcat/<int:catid>/', views.modcat, name='modcat'),
    path('delmov/<int:movid>/', views.delmov, name='delmov'),
    path('modmov/<int:movid>/', views.modmov, name='modmov'),
    path('viewmodprofile/', views.viewmodprofile, name='viewmodprofile'),
    path('modprofile/', views.modprofile, name='modprofile'),
    path('chgpwd/', views.chgpwd, name='chgpwd'),
    path('findmovies/', views.findmovies, name='findmovies'),
    path('ratenreview/<int:movid>/', views.ratenreview, name='ratenreview'),
    path('addfav/<int:movid>/', views.addfav, name='addfav'),
    path('movcatwise/', views.movcatwise, name='movcatwise'),
    path('favs/', views.favs, name='favs'),
    path('seerevrat/<int:movid>/', views.seerevrat, name='seerevrat'),


]