from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.core.exceptions import ValidationError
from .forms import RegForm, LoginForm
from django.contrib.auth.models import User
from django.views.generic import View
from django.views import generic
from django.contrib.auth import authenticate, login
from django.contrib import messages
from home.models import UserBooks
from django.contrib.sessions.models import Session
from bokeh.io import output_file,show,output_notebook,push_notebook
from bokeh.plotting import figure
from bokeh.models import ColumnDataSource,HoverTool,CategoricalColorMapper
from bokeh.layouts import row,column,gridplot
from bokeh.models.widgets import Tabs,Panel
from bokeh.embed import components
from bokeh.resources import CDN
from bokeh.models import CustomJS, ColumnDataSource, HoverTool
from math import pi
# Create your views here.
def MainPage(request):
    usercount=User.objects.filter(username__contains='').count()
    bookcount = UserBooks.objects.filter(book_name__contains='').count()
    onlinecount=Session.objects.filter(session_key__contains='').count()
    p = figure(plot_width=400, plot_height=250, x_axis_type="datetime")
    result = []
    for temp in range(1, 11):
        result.append(UserBooks.objects.filter(book_rating=temp).count())
        hover_tool = HoverTool()
        hover_tool2 = HoverTool()
    p1= figure(x_axis_label='Rating',y_axis_label='No.Of.Books',plot_width=400,plot_height=250,tools= [hover_tool,"crosshair,pan,reset"])

    items=UserBooks.objects.order_by('book_genre').values('book_genre').distinct()
    res=[]
    val=[]
    for temp in items:
        for key,value in temp.items():
            res.append(value)
            val.append(UserBooks.objects.filter(book_genre=value).count())

    p2 = figure(x_axis_label='No Of Books',y_axis_label='Genres', y_range=res,plot_width=400, plot_height=250,tools=[hover_tool2,"crosshair,pan,reset"])

    p.line([1,2,3,4,5], [4,1,3,5,2], color='navy', alpha=0.5)
    p1.vbar(x=[1,2,3,4,5,6,7,8,9,10], top=result,width=0.5, color='navy', alpha=0.75)
    p2.hbar(y=res, right=val,height=0.5,line_width=1,color='navy', alpha=0.75)
    p2.xaxis.major_label_orientation = pi / 4
    script, div = components(p)
    script1,div1=components(p1)
    script2,div2=components(p2)
    return render(request,'mainpage.html',{'usercount':usercount,'bookcount':bookcount,'onlinecount':onlinecount,'script':script,'div':div,'script1':script1,'div1':div1,'script2':script2,'div2':div2})


class UserFormView(View):
    form_class = RegForm
    template_name = 'signup.html'

    def get(self, request):
        form = self.form_class()
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = self.form_class(request.POST)
        if (form.is_valid()):
            user = form.save(commit=False)
            password=form.cleaned_data['password']
            user.set_password(password)
            user.save()
            return redirect('login')
        return render(request, self.template_name, {'form': form})

def login_view(request):
    if (request.method == 'POST'):
        form = LoginForm(data=request.POST)
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)

        if (user is not None):
            login(request, user)
            return redirect('/home')
        else:
            messages.error(request, "Enter a valid username or password")
    else:
        form = LoginForm()
    return render(request, 'accounts/login.html', {'form': form})

def logout_view(request):
    del request.session['username']
    return render(request,'/')
