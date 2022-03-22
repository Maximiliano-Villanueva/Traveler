from django.shortcuts import render
from django.http import HttpResponse
from Fligts.forms.search_form import SearchForm
# Create your views here.

def index(request):
    return HttpResponse("Hello World")

def intro(request):
    name = request.GET.get('name', 'test')
    params = {'name' : name, 'elements' : list(range(10))}

    return render(request, "intro.html", params)


def finder(request):

    form = SearchForm(request.POST)
    params = {'form' : form}

    if not form.is_valid():
        #add error class to fields with error
        for field, error_str in form.errors.items():

            if 'class' in form[field].field.widget.attrs:
                form[field].field.widget.attrs['class'] += ' error '
            else:
                form[field].field.widget.attrs['class'] = ' error '

 
    

    return render(request, "finder.html", params)