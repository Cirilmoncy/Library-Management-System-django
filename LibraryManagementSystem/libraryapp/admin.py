from django.contrib import admin
from .models import *


# Register your models here.

admin.site.register(StudentDetails)
admin.site.register(LibraryBookDetail)
admin.site.register(BookRequest)
admin.site.register(AcceptedBook)