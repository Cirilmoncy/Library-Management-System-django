from django.db.models.query import QuerySet
from django.shortcuts import render,HttpResponse,redirect
from django.views import generic
from .forms import *
from django.urls import reverse_lazy
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login,authenticate
from .models import *

from django.shortcuts import get_object_or_404
# Create your views here.

class index(generic.View):
    template_name='index.html'
    success_url=reverse_lazy('index')


class studentreg(generic.CreateView):
    form_class = studregform
    template_name = 'student.html'
    success_url = reverse_lazy('slogin')
    def form_valid(self, form):
        user =form.save(commit=False)
        password=form.cleaned_data['password']
        user.set_password(password)
        user.save()

        department=form.cleaned_data['depart                                               ment']
        rollno=form.cleaned_data['roll_no']
        regid=form.cleaned_data['register_id']
        phone=form.cleaned_data['phone']
        college=form.cleaned_data['college_name']
        StudentDetails.objects.create(user=user,department=department,phone=phone,roll_no=rollno,register_id=regid,college_name=college)
        return super().form_valid(form)


class studlogin(generic.View):
    form_class=AuthenticationForm
    template_name='studlogin.html'
    def get(self,request):
        data=User.objects.all()
        for i in data:
            request.session['userid']=i.id
        form=AuthenticationForm
        return render(request,'studlogin.html',{'form':form})
    def post(self,request):
        form=AuthenticationForm(request,data=request.POST)
        if form.is_valid():
            username=form.cleaned_data.get('username')
            password=form.cleaned_data.get('password')
            user=authenticate(username=username,password=password)
            if user is not None:
                login(request,user)
                return redirect('profile')
            else:
                return HttpResponse('Invalid credentials...')
        else:
            return HttpResponse('Form is invalid...')

def success(request):
    return render(request,'success.html')


class ProfileView(generic.DetailView):
    model = StudentDetails  # Because studentDetails create a oneto one connection with User model
    template_name = 'profile.html'
    context_object_name = 'profile'
    def get_object(self):
        # userid=self.request.session['userid']
        # return StudentDetails.objects.get(user_id=userid)

        # or

        user = self.request.user    # this is the method that is used to get the details of current logged in user
        return get_object_or_404(StudentDetails,user=user)

        # it return studentdetails that matches the user datas that are loggedin



# class StudentEdit(generic.UpdateView):
#     model = StudentDetails
#     template_name = 'studentedit.html'
#     fields =['username','first_name','last_name','email','phone','department','roll_no','register_id','college_name']
#     success_url = reverse_lazy('profileview')


class StudentEdit(generic.UpdateView):
    model = User
    form_class = EditProfileForm
    template_name = 'studentedit.html'
    success_url = reverse_lazy('profile')
    def get_object(self):   # its a built in function to get primarykey /attributes
        user=super().get_object()   # method used to get datas into the user(primarykey),
                                    # here  i get the object with the specific id passing intoo the url
        self.StudentDetails_instance=StudentDetails.objects.get(user=user)
                                            # store corresponding data in each instances.
                                            # Because the instance value which is used in django
                                            #    forms to specify which particular instance the form is prefilled.
                                            #    What happens is that the form is filled with the data from the articular record
        return user

    def get_form(self,form_class=None):
        form=super().get_form(form_class) # get StudentEditForm
        form.fields['phone'].initial=self.StudentDetails_instance.phone
        form.fields['department'].initial = self.StudentDetails_instance.department
        form.fields['roll_no'].initial = self.StudentDetails_instance.roll_no
        form.fields['register_id'].initial = self.StudentDetails_instance.register_id
        form.fields['college_name'].initial = self.StudentDetails_instance.college_name
        return form


    def form_valid(self, form): # pass geted form from get_form
        response=super().form_valid(form)
        self.StudentDetails_instance.phone = form.cleaned_data['phone']
        self.StudentDetails_instance.department=form.cleaned_data['department']
        self.StudentDetails_instance.roll_no = form.cleaned_data['roll_no']
        self.StudentDetails_instance.register_id = form.cleaned_data['register_id']
        self.StudentDetails_instance.college_name = form.cleaned_data['college_name']
        self.StudentDetails_instance.save()
        return response

class Add_Book(generic.CreateView):
    form_class = libbookform
    template_name = 'addbook.html'
    success_url = reverse_lazy('success')

class LibBooksView(generic.ListView):
    model = LibraryBookDetail
    template_name = 'booksview.html'
    context_object_name ='data'

class StudentBooksView(generic.ListView):
    model = LibraryBookDetail
    template_name = 'studviewbooks.html'
    context_object_name = 'data'

class BoolDelete(generic.DeleteView):
    model = LibraryBookDetail
    template_name = 'delete.html'
    success_url = reverse_lazy('booksview')

class BookView(generic.DetailView):
    model = LibraryBookDetail
    template_name = 'detailbookview.html'

class StudentBookDetail(generic.DetailView):
    model = LibraryBookDetail
    template_name = 'studbookdetail.html'
class BookUpdate(generic.UpdateView):
    model = LibraryBookDetail
    template_name = 'bookupdate.html'
    fields = ['book_name','book_img','auther','book_id','description','available_copies']
    success_url = reverse_lazy('booksview')


class CreateBookRequestView(generic.View):
    def get(self,request,pk):
        book=get_object_or_404(LibraryBookDetail,pk=pk)
        user_detail=get_object_or_404(StudentDetails,user=request.user)

        #   Check if the user has already requested this book
        if BookRequest.objects.filter(user=user_detail,book=book).exists():
            return HttpResponse("You have already requested this book.")
        else:
            BookRequest.objects.create(user=user_detail,book=book)
            return HttpResponse("Your request has been sent.")

class DisplayRequestedBooks(generic.ListView):
    model = BookRequest
    template_name = 'requestedbooks.html'
    context_object_name = 'requested_books'
    #   you can override your query in listview using get_queryset
    def get_queryset(self):
        user=self.request.user
        return BookRequest.objects.filter(user__user__id=user.id)


class LibraryRequestViewStudent(generic.ListView):
    model = BookRequest
    template_name = 'libraryrequest_view.html'
    context_object_name = 'request_data'

from datetime import timedelta
from django.utils import timezone

class AcceptBookRequestView(generic.View):
    def get(self,request,pk,accepted_date=None):
        book_request=get_object_or_404(BookRequest,pk=pk)
        accepted_book=AcceptedBook.objects.create(
            details=book_request.details,
            fine=0,
            return_date=timezone.now()+timedelta(days=10),
        request_date=book_request.request_date    
        )
        accepted_date=accepted_book.accepted_date
        current_date=timezone.now()
        return_date=accepted_date+timedelta(days=5)

        fine=0  # store incremented data

        if current_date > return_date:
            overdue_days=(current_date - return_date).days
            fine=overdue_days*10
            accepted_book.return_date=return_date
            accepted_book.fine=fine
        accepted_book.save()
            

        return HttpResponse('Accepted')
    



class AcceptedButton(generic.View):
    def get(self,request,pk):
        book_request=get_object_or_404(BookRequest,id=pk)

        AcceptedBook.objects.create(
            bookname=book_request.book_name,
            Author=book_request.author,
            requestdate=book_request.request_date,
            userdetails=book_request.details,
            return_date=timezone.now()+timedelta(days=10)
        )
        book_request.delete

        return HttpResponse('cancel')
    

class Accepted_lidt_view(generic.ListView):
    model=AcceptedBook
    template_name='accepted book_list.html'
    context_object_name='data'

    def get_queryset(self):
        queryset=super().get_queryset()
        current_date=timezone.now()
        # data preprocess
        for accepted_book in queryset:
            if current_date>accepted_book.return_date:
                overdue_days=(current_date-accepted_book.return_date).days
                accepted_book.fine=overdue_days*10
            else:
                accepted_book.fine=0
            accepted_book.save()

        return queryset             
          
