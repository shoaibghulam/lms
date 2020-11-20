from django.contrib import admin
from .models import BookAuthor,Books
# Register your models here.
class BookAuthorAdmin(admin.ModelAdmin):
    list_display=("BookAuthorFirstName","BookAuthorLastName")

class BookAdmin(admin.ModelAdmin):
    list_display=('BookTitle','BookAuthorid','BookEdition','BookPublisher','BookYearOfPublisher','BookISBN','Bookcategory')

admin.site.register(BookAuthor,BookAuthorAdmin)
admin.site.register(Books,BookAdmin)
