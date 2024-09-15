from django.shortcuts import render, redirect
from .models import Recipe
from django.http import HttpResponse, JsonResponse, HttpResponseRedirect
from django.contrib.auth import login, authenticate
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth import logout

# View for displaying and creating recipes
@login_required(login_url='/login/')
def recipes(request):
    if request.method == 'POST':
        data = request.POST
        day = data.get('day')
        name = data.get('name')
        description = data.get('description')

        # Create a new recipe
        Recipe.objects.create(
            day=day,
            name=name,
            description=description,
        )
        return redirect('/')
    
    # Retrieve and filter recipes
    queryset = Recipe.objects.all()
    if request.GET.get('search'):
        queryset = queryset.filter(day__icontains=request.GET.get('search'))  # Fixed filter typo
    context = {'recipes': queryset}
    return render(request, 'recipe.html', context)

# View for updating a recipe
@login_required(login_url='/login/')
def update_recipe(request, id):
    queryset = Recipe.objects.get(id=id)  # Fixed 'object' typo

    if request.method == 'POST':  # Fixed 'metod' typo
        data = request.POST
        day = data.get('day')
        name = data.get('name')
        description = data.get('description')

        # Update the recipe details
        queryset.day = day
        queryset.name = name
        queryset.description = description
        queryset.save()
        return redirect('/')
    
    context = {'recipe': queryset}
    return render(request, 'update_recipe.html', context)  # Fixed template name typo

# View for deleting a recipe
@login_required(login_url="/login/")
def delete_recipe(request, id):
    queryset = Recipe.objects.get(id=id)
    queryset.delete()
    return redirect('/')

# View for user login
def login_page(request):
    if request.method == 'POST':
        try:
            username = request.POST.get('username')
            password = request.POST.get('password')
            
            # Check if user exists
            user_obj = User.objects.filter(username=username)
            if not user_obj.exists():
                messages.error(request, "Username not found")
                return redirect('/login')

            # Authenticate user
            user_obj = authenticate(username=username, password=password)
            if user_obj:
                login(request, user_obj)
                return redirect('recipes')
            messages.error(request, "Wrong password")
            return redirect('/login/')
        
        except Exception as e:
            messages.error(request, "Something went wrong")
            return redirect('/register/')
    
    return render(request, "login.html")

# View for user registration
def register_page(request):
    if request.method == 'POST':
        try:
            username = request.POST.get('username')
            password = request.POST.get('password')
            
            # Check if username already exists
            user_obj = User.objects.filter(username=username)
            if user_obj.exists():
                messages.error(request, 'Username is already taken')
                return redirect('/register/')
            
            # Create a new user
            user_obj = User.objects.create(username=username)
            user_obj.set_password(password)
            user_obj.save()
            messages.success(request, "Account created")
            return redirect('/login')
        
        except Exception as e:
            messages.error(request, "Something went wrong")
            return redirect('/register')
    
    return render(request, "register.html")

# View for user logout
def custom_logout(request):
    logout(request)
    return redirect('login')

# View for displaying recipes in PDF format
@login_required(login_url='/login/')
def pdf(request):
    if request.method == 'POST':
        data = request.POST    
        day = data.get('day')
        name = data.get('name')
        description = data.get('description')

        # Create a new recipe
        Recipe.objects.create(
            day=day,
            name=name,
            description=description,
        )
        return redirect('pdf')
    
    queryset = Recipe.objects.all()

    # Search functionality
    if request.GET.get('search'):
        queryset = queryset.filter(day__icontains=request.GET.get('search'))  # Fixed filter typo
    
    context = {'recipes': queryset}
    return render(request, 'pdf.html', context)
def home(request):
    return render(request, 'home.html') 
def recipe_list(request):
    recipes = Recipe.objects.all()
    return render(request, 'recipe_list.html', {'recipes': recipes}) 

