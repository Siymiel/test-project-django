from django.contrib import admin
from .models import Book
import datetime
from pytz import timezone

# Register your models here.
class BookAdmin(admin.ModelAdmin):
   
    list_filter = ["published_date"]

    list_display = ['title', 'author', 'price', 'published_date', 'stock']
    
    search_fields = ["title", "author"]
    
admin.site.register(Book, BookAdmin)