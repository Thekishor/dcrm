from django.shortcuts import redirect, render
from django.contrib.auth import authenticate,login, logout
from django.contrib import messages
from .forms import SignUpForm, AddRecordForm
from .models import Record

#from webapp.forms import SignUpForm

# Create your views here.
def home(request):
  
  records = Record.objects.all()
  
  #check to see if logging in
  if request.method == 'POST':
    username = request.POST['name']
    password = request.POST['password']
    
   #Autheticate
    user = authenticate(request, username=username, password=password)
    if user is not None:
      login(request, user)
      messages.success(request, "You have been Logeed In successful !")
      return redirect('home')
    else:
      messages.success(request, "There was An Error In Logeed In , Please try Again.. ")
      return redirect('home')
  else:
    return render(request, 'home.html', {'records': records})

def logout_user(request):
  logout(request)
  messages.success(request, "You Have Been Logged Out...........")
  return redirect('home')

def register(request):
  if request.method == 'POST':
    form = SignUpForm(request.POST)
    if form.is_valid():
      form.save()
      
      #Authenticate and loggin
      username = form.cleaned_data['username']
      password = form.cleaned_data['password1']
      user = authenticate(username=username, password=password)
      login(request, user)
      messages.success(request, "You Have Successfully Registered !")
      return redirect('home')
  else:
    form = SignUpForm()
    return render(request, 'register.html', {'form': form})
  
  return render(request, 'register.html', {'form': form})

def record(request, pk):
  if request.user.is_authenticated:
    records = Record.objects.get(id=pk)
    return render(request, 'record.html', {'records': records})
  
  else:
    messages.success(request, "You Must be Logged In To View That Page")
    return redirect('home')

def delete_record(request, pk):
    if request.user.is_authenticated:
      delete_user = Record.objects.get(id=pk)
      delete_user.delete()
      messages.success(request, "Record Deleted Successfully...")
      return redirect('home')
    else:
      messages.success(request, "You Must Be Logged In To Do That...")
      return redirect('home')
    
def add_record(request):
  form = AddRecordForm(request.POST or None)
  if request.user.is_authenticated:
    if(request.method=="POST"):
      if form.is_valid():
        add_record = form.save()
        messages.success(request, "Record Added...")
        return redirect('home')  
    return render(request,'add_record.html',{'form': form})
  else:
    messages.success(request, "You Must Be Logged In...")
    return redirect('home')
  
def update_record(request, pk):
  if request.user.is_authenticated:
    current_record = Record.objects.get(id=pk)
    form = AddRecordForm(request.POST or None, instance=current_record)
    if form.is_valid():
      form.save()
      messages.success(request, "Record Has Been Updated...")
      return redirect('home')
    return render(request, 'update_record.html', {'form': form}) 
  else:
    messages.success(request, "You Must Be Logged In To Do That...")
    return redirect('home') 