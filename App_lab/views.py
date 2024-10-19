from django.shortcuts import render
def home(request):
 return render(request,'home.html',{'name':'Harshini'})

def add(request):
    try:
        val1 = int(request.POST.get('num1', 0))
        val2 = int(request.POST.get('num2', 0))
        val3 = val1 + val2
    except ValueError:
        val3 = "Invalid input! Please enter valid numbers."
    return render(request,'result.html',{'result':val3})
# Create your views here.

def dashboard(request):
 return render(request,'dashboard.html')
