from django.shortcuts import render,redirect
from django.http import HttpResponse
from django.views.generic.edit import FormView
from . forms import BookForm,ImageUploadForm
from django.contrib.auth.models import User
from . models import UserBooks
from django.contrib.auth.models import User
from django.views import generic
from django.contrib.auth.decorators import login_required
from .models import UserBooks,FavBooks,BooksIsbn,Images
from django.shortcuts import get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse
from bokeh.io import output_file,show,output_notebook,push_notebook
from bokeh.plotting import figure
from bokeh.models import ColumnDataSource,HoverTool,CategoricalColorMapper
from bokeh.layouts import row,column,gridplot
from bokeh.models.widgets import Tabs,Panel
from bokeh.embed import components
from bokeh.resources import CDN
from bokeh.models import CustomJS, ColumnDataSource, HoverTool
from math import pi
import csv
@login_required
def HomeView(request):
    flag = Images.objects.filter(user_id=request.user).exists()
    topbooks = UserBooks.objects.order_by('-book_rating')[:5]
    obj=0
    if (flag):
        obj = Images.objects.get(user_id=request.user)
    hover_tool = HoverTool()
    p = figure(x_axis_label='Rating', y_axis_label='No.Of.Books', plot_width=400, plot_height=250,tools=[hover_tool, "crosshair,pan,reset"])
    bookgenres = UserBooks.objects.order_by('book_genre').values('book_genre').distinct()
    user = User.objects.get(pk=request.user.id)
    gen = set()
    userbooks = user.userbooks_set.all()
    for books in userbooks:
        gen.add(books.book_genre)
    gen = list(gen)
    result = []
    for temp in gen:
        result.append(user.userbooks_set.filter(book_genre=temp).count())
    hover_tool = HoverTool()
    p1 = figure(x_axis_label='Genre', y_axis_label='No.Of.Books', x_range=gen, plot_width=400, plot_height=250,
               tools=[hover_tool, "crosshair,pan,reset"])
    p1.vbar(x=gen, top=result, width=0.5, color='navy', alpha=0.75)
    p1.xaxis.major_label_orientation = pi / 4
    script1, div1 = components(p1)
    if(request.method=='POST'):
        str=request.POST['topbook']
        result=[]
        for i in range(1, 11):
            result.append(UserBooks.objects.filter(book_genre=str).filter(book_rating=i).count())
        topbooks=UserBooks.objects.filter(book_genre__contains=str).order_by('-book_rating')[:5]
        p.vbar(x=[1, 2, 3, 4, 5, 6, 7, 8, 9, 10], top=result, width=0.5, color='navy', alpha=0.75)
        script,div=components(p)
        genre=str
        return render(request, 'home/homepage.html',{'flag': flag, 'obj': obj, 'topbooks': topbooks, 'bookgenres': bookgenres,'script':script,'div':div,'script1':script1,'div1':div1,'genre':genre})

    return render(request, 'home/homepage.html',{'flag': flag, 'obj': obj, 'topbooks': topbooks, 'bookgenres': bookgenres,'script1':script1,'div1':div1})

class BookDetailsView (LoginRequiredMixin,generic.DetailView):
    model=UserBooks
    template_name='home/bookdetails.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['books'] = self.request.user.userbooks_set.all
        context['favorites']=self.request.user.favbooks_set.all
        context['flag']=True
        context['popular']=UserBooks.objects.filter(book_genre=super().get_object().book_genre).order_by('-book_rating')[:5]
        return context


class BooksView (LoginRequiredMixin,generic.DetailView):
     model=User
     template_name='home/mybooks.html'

     def get_object(self):
         return self.request.user

class WishlistView (LoginRequiredMixin,generic.DetailView):
    model=User
    template_name='home/wishlist.html'

    def get_object(self):
         return self.request.user

@login_required
def SearchedBooks(request):
   if(request.method=='GET'):
       item=request.GET['q']
       flag=request.GET['NAME']
       if(flag=='1'):
           setvalues=UserBooks.objects.filter(book_name__contains=item)
           return render(request,'home/search.html',{'setvalues':setvalues,'flag':1})
       if (flag == '2'):
           setvalues = User.objects.filter(username__contains=item)
           return render(request, 'home/search.html', {'setvalues': setvalues, 'flag': 2})
       if (flag == '3'):
           setvalues = UserBooks.objects.filter(book_ISBN__contains=item)
           return render(request, 'home/search.html', {'setvalues': setvalues, 'flag': 3})
       if (flag == '4'):
           setvalues = UserBooks.objects.filter(book_author__contains=item)
           return render(request, 'home/search.html', {'setvalues': setvalues, 'flag': 4})


@login_required
def addBooks(request):
    if (request.method=='POST'):
        form=BookForm(data=request.POST)
        if(form.is_valid()):
            u=UserBooks()
            u.book_name=form.cleaned_data['book_name']
            u.book_author=form.cleaned_data['book_author']
            u.book_ISBN=form.cleaned_data['book_ISBN']
            u.book_status=True
            u.book_genre=form.cleaned_data['book_genre']
            u.username=request.user.username
            u.user_id = User.objects.get(username=request.user.username)
            u.book_url= form.cleaned_data['book_url']
            u.save()
            return redirect('/home')
    else:
        form = BookForm()
    return render (request,'home/addbooks.html',{'form':form})


def favorite_ajax(request):
    data = {'success': False}
    if request.method == 'POST':
        book = request.POST.get('userbooks')
        fav = FavBooks()
        book_id = UserBooks.objects.get(pk=book)
        user_id = request.user
        if(FavBooks.objects.filter(user_id=user_id, book_id=book_id).exists()):
                data['success']=False
                return JsonResponse(data)
        fav.book_id = book_id
        fav.user_id = user_id
        fav.save()
        data['success']=True
    return JsonResponse(data)
def removefavorite_ajax(request):
    data = {'success': False}
    if request.method == 'POST':
        book = request.POST.get('userbooks')
        fav = FavBooks()
        book_id = UserBooks.objects.get(pk=book)
        user_id = request.user
        if(FavBooks.objects.filter(user_id=user_id, book_id=book_id).exists()):
                FavBooks.objects.get(user_id=user_id, book_id=book_id).delete()
                data['success']=True
                return JsonResponse(data)

        data['success']=False
    return JsonResponse(data)

def deleteBook(request):
    if (request.method =='POST'):
        userbook=request.POST['userbook']
        UserBooks.objects.get(pk=userbook).delete()
        return redirect('home:myBooks')

def uploadPic(request):
    if request.method == 'POST':
        form = ImageUploadForm(request.POST, request.FILES)
        if form.is_valid():
            m=form.save(commit=False)
            m.user_id=request.user
            m.save()
            return redirect('home:home')
        else:
            return HttpResponse("validation fails")
    else:
        form = ImageUploadForm()
        return render(request,'home/uploadpic.html',{'form':form})


def UsersBooksView(request,pk):

    obj=get_object_or_404(User,pk=pk)
    return render(request,'home/mybooks.html',{'user':obj})
# Create your views here.
