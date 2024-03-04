from django.contrib import admin
from .models import Movie,Category,Rating,Favorites
# Register your models here.
admin.site.register(Category)
admin.site.register(Movie)
admin.site.register(Rating)
admin.site.register(Favorites)
