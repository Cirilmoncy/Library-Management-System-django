from django.urls import path
from .views import *

urlpatterns=[
    path('studentregister/',studentreg.as_view(),name='student'),
    path('studlogin/',studlogin.as_view(),name='slogin'),
    path('profileview/',ProfileView.as_view(),name='profile'),
    path('addbook/',Add_Book.as_view(),name='addbook'),
    path('booksview/',LibBooksView.as_view(),name='booksview'),
    path('bookdelete/<pk>',BoolDelete.as_view(),name='bookdelete'),
    path('bookdetail/<pk>',BookView.as_view(),name='bookview'),
    path('bookupdate/<pk>',BookUpdate.as_view(),name='bookupdate'),
    path('studbooksview/',StudentBooksView.as_view(),name='studbookview'),
    path('studbookdetail/<pk>',StudentBookDetail.as_view(),name='studbookdetail'),
    path('studentedit/<pk>',StudentEdit.as_view(),name='studentedit'),
    path('request/<pk>',CreateBookRequestView.as_view(),name='create_request'),
    path('requestedbooks/',DisplayRequestedBooks.as_view(),name='requestedbooks'),
    path('libraryrequestview/',LibraryRequestViewStudent.as_view(),name='librequestviewstud'),
    path('successmsg/',success,name='success'),
    path('index/',index.as_view(),name='index'),
]