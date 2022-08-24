from django.shortcuts import render
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required
import json
from django.http import HttpResponse
import requests
from .models import CityWeather
from django.conf import settings

# Create your views here.
def LoginPage(request):
    if request.user.is_authenticated:
        # If the user is already logged in, then redirect him to the dashboard
        return redirect('dashboard')
    else:
        if request.method == 'POST':
            username = request.POST.get('username')
            password =request.POST.get('password')
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('dashboard')
            else:
                messages.warning(request, 'Please Enter the valid Username and Password')
    context = {}
    return render(request, 'account/login.html', context)



@login_required(login_url='user_login')
def Dashboard(request):
    # This view will be the landing page after successfull login
    return render(request, 'account/dashboard.html')
    


@login_required(login_url='user_login')
def SearchCity(request):
    #This function will call the accouweather API to search for cities
    q = request.GET.get("term") # The autocomplete term/city name to be searched
    
    result = []
    data={}

    # call accuweather API for info start
    apikey = settings.ACCUWEATHER_APIKEY
    payload = {'apikey': apikey, 'q': q, 'language': 'en-us'}
    
    r = requests.get('http://dataservice.accuweather.com/locations/v1/cities/search', payload)
    print(r)
    if r.status_code == 200:
        json_data = str(r.json())
        dict_data = json.loads(r.text)

        for item in dict_data:
            if item:
                data['id'] = item['Key']
                data['value'] = item['LocalizedName']+" "+item['Country']['LocalizedName']
                result.append(data)
    else:
        data['id'] = 0
        data['value'] = 'Some Error'
        result.append(data)

    

    dump=json.dumps(result)
    # call accuweather API for info end

    return HttpResponse(dump,'application/json')


@login_required(login_url='user_login')
def GetWeatherInfo(request):
    #take the city key in the request and call the accuweather API to get the weather informations
    city_key = request.POST.get("city_key")
    city_name = request.POST.get("city_name")

    # call accuweather API for info start
    apikey = settings.ACCUWEATHER_APIKEY
    payload = {'apikey': apikey, 'language': 'en-us'}
    r = requests.get('http://dataservice.accuweather.com/forecasts/v1/daily/1day/'+city_key, payload)
    json_data = str(r.json())
    dict_data = json.loads(r.text)
    
    # call accuweather API for info end

    # For display purpose 
    day_precipitation = 'NO'
    if dict_data["DailyForecasts"][0]["Day"]["HasPrecipitation"]:
        day_precipitation = 'YES'

    night_precipitation = 'NO'
    if dict_data["DailyForecasts"][0]["Night"]["HasPrecipitation"]:
        night_precipitation = 'YES'

    resp_data = {
        "headline_text": dict_data["Headline"]["Text"],
        "dailyfc_date": dict_data["DailyForecasts"][0]["Date"],
        "temperature_min_val": dict_data["DailyForecasts"][0]["Temperature"]["Minimum"]["Value"],
        "temperature_min_unit": dict_data["DailyForecasts"][0]["Temperature"]["Minimum"]["Unit"],
        "temperature_max_val": dict_data["DailyForecasts"][0]["Temperature"]["Maximum"]["Value"],
        "temperature_max_unit": dict_data["DailyForecasts"][0]["Temperature"]["Maximum"]["Unit"],
        "day_conditions": dict_data["DailyForecasts"][0]["Day"]["IconPhrase"],
        "day_precipitation": day_precipitation,
        "night_conditions": dict_data["DailyForecasts"][0]["Night"]["IconPhrase"],
        "night_precipitation": night_precipitation
    }

    # store above info in table start
    try:
        already_exists = CityWeather.objects.get(city_key = city_key, forecast_date = resp_data["dailyfc_date"])
    except Exception as e:
        already_exists = None
    
    if not already_exists:
        CityWeather.objects.create(
            city_key = city_key,
            city_name = city_name,
            forecast_date = resp_data["dailyfc_date"],
            headline = resp_data["headline_text"],
            temperature_min_val = resp_data["temperature_min_val"],
            temperature_min_unit = resp_data["temperature_min_unit"],
            temperature_max_val = resp_data["temperature_max_val"],
            temperature_max_unit = resp_data["temperature_max_unit"],
            day_conditions = resp_data["day_conditions"],
            day_precipitation = dict_data["DailyForecasts"][0]["Day"]["HasPrecipitation"],
            night_conditions = resp_data["night_conditions"],
            night_precipitation = dict_data["DailyForecasts"][0]["Night"]["HasPrecipitation"]
        )
    # store above info in table end


    return HttpResponse(json.dumps(resp_data), content_type="application/json")


@login_required(login_url='user_login')
def AllWeatherDetails(request):
    # This function simply displays all the cities into tabular structure.
    city_weathers = CityWeather.objects.all().order_by("-id")
    data = {
        "city_weathers": city_weathers
    }
    return render(request, 'account/all-weather-details.html', data)


def logoutUser(request):
    logout(request)
    return redirect('/account/login/')