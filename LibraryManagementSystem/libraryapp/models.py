from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class StudentDetails(models.Model):
    user=models.OneToOneField(User,on_delete=models.CASCADE)
    department=models.CharField(max_length=15)
    phone=models.IntegerField()
    roll_no=models.IntegerField()
    register_id=models.CharField(max_length=10)
    college_name=models.CharField(max_length=20)
    def __str__(self):
        return self.department

class LibraryBookDetail(models.Model):
    book_name=models.CharField(max_length=20)
    book_img=models.ImageField(upload_to='image/')
    auther=models.CharField(max_length=20)
    book_id=models.CharField(max_length=10)
    description=models.CharField(max_length=100)
    available_copies=models.IntegerField()
    def __str__(self):
        return self.book_name


class BookRequest(models.Model):
    user=models.ForeignKey(StudentDetails,on_delete=models.CASCADE)
    book=models.ForeignKey(LibraryBookDetail,on_delete=models.CASCADE)
    request_date=models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Request by {self.user.user.username} for {self.book.book_name}"


class AcceptedBook(models.Model):
    # user=models.ForeignKey(StudentDetails,on_delete=models.CASCADE)
    # book=models.ForeignKey(LibraryBookDetail,on_delete=models.CASCADE)
    book_name=models.CharField(max_length=20)
    author=models.CharField(max_length=20)
    details=models.ForeignKey(StudentDetails,on_delete=models.CASCADE)
    request_date=models.DateTimeField()
    accepted_date=models.DateTimeField(auto_now_add=True)
    fine=models.IntegerField(default=0)
    return_date=models.DateTimeField()

    def __str__(self):
        return f"Request by {self.user.user.username} for {self.book.book_name}"

