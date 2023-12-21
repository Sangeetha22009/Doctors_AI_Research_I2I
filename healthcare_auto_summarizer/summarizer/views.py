import pdb
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from .forms import UserRegistrationForm
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
import requests

# Create your views here.
# @login_required(login_url='login')
def index(request):
    return render(request, "summarizer/index.html")

def user_login(request):
    if request.user.is_authenticated:
        return redirect('summarizer')
    else:
        if request.method == 'POST':
            name = request.POST.get('username')
            password = request.POST.get('password')
            user = authenticate(request, username=name, password=password)
            if user is not None:
                login(request, user)                
                return redirect('summarizer')
            else:
                messages.error(request, "Inavlid User Name or Password")
        return render(request, "summarizer/login.html")
def user_logout(request):
    if request.user.is_authenticated:
        logout(request)
    return redirect('/')

def register(request):
    registraion_form = UserRegistrationForm()
    if request.method == 'POST':
        registraion_form = UserRegistrationForm(request.POST)
        if registraion_form.is_valid():
            registraion_form.save()
            messages.success(request, 'Registered Successfuly, Please Login..')
            return redirect('/login')
    return render(request, "summarizer/register.html", {'registraion_form': registraion_form})

def summarizer(request):
    if request.user.is_authenticated:
        if request.method == 'POST':
            user_input = request.POST.get('search_text')
            selected_option = request.POST.get('response_way', '')  
            fastapi_url=''
            resulting_list = list[str]
            # pdb.set_trace()       
            # Request to FastAPI endpoint
            if(selected_option == 'Summarize'):
                fastapi_url = 'http://127.0.0.1:9898/summarize'
                resulting_list = str(user_input).split(',')
                print(resulting_list)
            elif(selected_option == 'Questionnaire'):
                fastapi_url = 'http://127.0.0.1:9898/query_reponse'
            response = requests.post(fastapi_url, json={'query_for_summarizer': user_input})
            # pdb.set_trace() 
            # print(f"response {response.json()}")            
            if response.status_code == 200:
                results = response.json()[0]
                # print(results)
                return render(request, 'summarizer/auto_summarizer.html', {'summarized_results': results})
            else:                
                return render(request, 'summarizer/auto_summarizer.html', {'error': 'Failed to get results'})
        return render(request, 'summarizer/auto_summarizer.html')
    else:
        return redirect('login')