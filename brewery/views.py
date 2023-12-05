# brewery/views.py
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect
from django.shortcuts import get_object_or_404
from django.http import JsonResponse
from .models import Brewery, Review
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login as auth_login
from django.contrib.auth.decorators import login_required
from .forms import ReviewForm
from django.contrib import messages
import requests
import json

############################################################################################

def brewery_search(request):
   if request.method == 'GET':
        # Get the search city from the query string
        search_city = request.GET.get('by_city', '')
        search_name = request.GET.get('by_name', '')
        search_type = request.GET.get('by_type','')
        
        # Construct the API URL with non-empty search parameters
        api_url = 'https://api.openbrewerydb.org/v1/breweries?per_page=3'
        if search_city:
            api_url += f'&by_city={search_city}'
        if search_name:
            api_url += f'&by_name={search_name}'
        if search_type:
            api_url += f'&by_type={search_type}'


        # Make a GET request to the Open Brewery DB API
        response = requests.get(api_url)

        if response.status_code == 200:
            breweries = response.json()
            return render(request, 'brewery/brewery_search.htm', {'breweries': breweries})
        else:
            error_message = f"Error: {response.status_code} - {response.text}"
            return render(request, 'brewery/brewery_search.htm', {'error_message': error_message})


   return render(request, 'brewery/brewery_search.htm')

##########################################################################################################


# Assuming this is your actual API endpoint for fetching brewery data
API_BASE_URL = 'https://api.openbrewerydb.org/v1/breweries/'

def get_brewery_data_from_api(brewery_id):
    api_url = f'{API_BASE_URL}{brewery_id}'
    response = requests.get(api_url)

    if response.status_code == 200:
        return response.json()
    else:
        # Handle API error, for example, raise an exception
        raise Exception(f"Error fetching brewery data from API: {response.status_code} - {response.text}")

# @login_required
def add_review(request, brewery_id):
    # Create a new Review instance
    if request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.user = request.user

            # Retrieve or create the Brewery instance based on the provided ID
            brewery, created = Brewery.objects.get_or_create(id=brewery_id)
            if created:
                # If the Brewery is newly created, you might want to populate its fields
                # using data from the API or other sources.
                brewery_data_from_api = get_brewery_data_from_api(brewery_id)
                brewery = Brewery.create_brewery_from_api_data(brewery_data_from_api)

            review.brewery = brewery
            review.save()
            return redirect('brewery_details', brewery_id=brewery_id)
    else:
        form = ReviewForm()

    return render(request, 'brewery/add_review.htm', {'form': form})

###########################################################################################################

@csrf_exempt
def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            # Save the user to the database
            user = form.save()

            # Log the user in using Django's auth_login
            user = authenticate(request, username=form.cleaned_data['username'], password=form.cleaned_data['password1'])
            auth_login(request, user)

            # Redirect to the home page or any other desired page
            return redirect('brewery_search')  # Replace 'home' with the name of your home page URL pattern
    else:
        form = UserCreationForm()

    return render(request, 'brewery/signup.htm', {'form': form})

@csrf_exempt
def custom_login(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, request.POST)
        if form.is_valid():
            user = form.get_user()
            auth_login(request, user)
            messages.success(request, 'Login successful.')
            return redirect('brewery_search')  # Redirect to the desired page after login
    else:
        form = AuthenticationForm()

    return render(request, 'brewery/login.htm', {'form': form})
