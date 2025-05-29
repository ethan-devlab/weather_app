# coding=utf-8
# from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django_ratelimit.decorators import ratelimit, Ratelimited
from django.utils import timezone
from .forms import *
import requests
import datetime
import time

# 032f175c8aad045f7655c1130fe7bbdf
# Create your views here.

try:
    @ratelimit(key='ip', rate='30/m', method=['GET', 'POST'])
    # @login_required(login_url='/weather_app/authentication')
    def index(request):
        was_limited = getattr(request, 'limited', False)
        # if request.COOKIES.get("visited") is None or str(request.COOKIES.get("visited")).lower() == "false" \
        #         or request.COOKIES.get('id_token') is None or request.COOKIES.get('id_token') == "":
        #     log_out(request)
        #     return redirect("/weather_app/authentication")
        # api_key = request.COOKIES.get('id_token')

        api_key = ""  # for testing purpose, put your api key here

        current_weather_url = 'https://api.openweathermap.org/data/2.5/weather?q={}&units=metric&appid={}'
        forecast_url = 'https://api.openweathermap.org/data/2.5/forecast?lat={}&lon={}&units=metric&appid={}'

        if request.method == 'POST':
            # if os.path.exists("data.json"):
            #     os.remove("data.json")

            city1 = request.POST['city1']
            city2 = request.POST['city2']

            try:
                # if city1 and city2:
                #     with open("data.json", )
                if city1:
                    weather_data1, daily_forecasts1 = fetch_weather_and_forecast(city1, api_key, current_weather_url,
                                                                                 forecast_url)
                else:
                    weather_data1, daily_forecasts1 = None, None

                if city2:
                    weather_data2, daily_forecasts2 = fetch_weather_and_forecast(city2, api_key, current_weather_url,
                                                                                 forecast_url)
                else:
                    weather_data2, daily_forecasts2 = None, None

                context = {
                    'weather_data1': weather_data1,
                    'daily_forecasts1': daily_forecasts1,
                    'weather_data2': weather_data2,
                    'daily_forecasts2': daily_forecasts2,
                }

                return render(request, 'index.html', context)

            except KeyError as e:
                error_alert(request, f"City not found, maybe city name can be more accurate or the API key is wrong.")
                return redirect('index')

        else:
            return render(request, 'index.html')

        # return render(request, 'weather_app/index.html')

    def fetch_weather_and_forecast(city, api_key, current_weather_url, forecast_url):
        response = requests.get(current_weather_url.format(city, api_key)).json()
        lat, lon = response['coord']['lat'], response['coord']['lon']
        forecast_response = requests.get(forecast_url.format(lat, lon, api_key)).json()
        weather_data = {
            'city': city,
            'country': response['sys']['country'],
            'temperature': response['main']['temp'],
            'feels_like': response['main']['feels_like'],
            'description': str(response['weather'][0]['description']).capitalize(),
            'icon': response['weather'][0]['icon'],
            'humidity': response['main']['humidity'],
            'visibility': round(response['visibility'] / 1000, 2),
            'wind_speed': round(response['wind']['speed'] * 3.6, 2),
            # 'precipitation': response['rain']['1h'],
            'cloudiness': response['clouds']['all'],
            'date': datetime.datetime.fromtimestamp(response['dt']).strftime('%b %d'),
            'time': datetime.datetime.fromtimestamp(response['dt']).strftime("%I:%M %p"),
            # 'id': response['id'],
            # 'api': api_key,
        }

        # if os.path.exists("data.json"):
        #     with open("data.json", "r", encoding="utf-8") as f:
        #         data = json.load(f)
        #         with open("data.json", "w", encoding="utf-8") as file:
        #             data['data'].append(weather_data)
        #             data_ = json.dumps(data, indent=2, ensure_ascii=False)
        #             file.write(data_)
        #
        # else:
        #     data_set = {
        #         "data": []
        #     }
        #
        #     data_set['data'].append(weather_data)
        #
        #     data = json.dumps(data_set, indent=2, ensure_ascii=False)
        #
        #     with open("data.json", "a", encoding="utf-8") as f:
        #         f.write(data)

        # print(forecast_response['list'])
        daily_forecasts = []
        for daily_data in forecast_response['list'][:25]:
            daily_forecasts.append({
                'day': datetime.datetime.fromtimestamp(daily_data['dt']).strftime('%A'),
                'date': datetime.datetime.fromtimestamp(daily_data['dt']).strftime("%b %d"),
                'time': datetime.datetime.fromtimestamp(daily_data['dt']).strftime("%I:%M %p"),
                'temperature': daily_data['main']['temp'],
                'description': str(daily_data['weather'][0]['description']).capitalize(),
                'icon': daily_data['weather'][0]['icon'],
                'humidity': daily_data['main']['humidity'],
                'visibility': round(daily_data['visibility'] / 1000, 2),
                'wind_speed': round(daily_data['wind']['speed'] * 3.6, 2),
                'wind_gust': round(daily_data['wind']['gust'] * 3.6, 2),
                'feels_like': daily_data['main']['feels_like'],
                'temp_min': daily_data['main']['temp_min'],
                'temp_max': daily_data['main']['temp_max'],
                'cloudiness': daily_data['clouds']['all'],
                'pop': round(daily_data['pop'] * 100, 2),
            })

        # DATA = load_data()
        # print(DATA['data'])
        return weather_data, daily_forecasts

    # def load_data():
    #     with open("data.json", "r", encoding='utf-8') as f:
    #         # print(json.loads(f.read()))
    #         return json.loads(f.read())
    def sign_up(request):
        form = AuthenticationForm()
        if request.method == 'POST':
            form = AuthenticationForm(request.POST)
            # api = request.POST.get('api')
            # data = valid(api)
            if form.is_valid():
                # status = data['cod']
                # if status == 200:
                form.save()
                messages.success(request, "註冊成功！Sign Up Successfully!")
                response = redirect('Authentication')
                time.sleep(3)
                return response
            else:
                error_alert(request, form.error_messages)

        context = {
            'form': form
        }

        return render(request, 'signup.html', context)


    def valid(key):

        url = f"https://api.openweathermap.org/data/2.5/weather?q=London&appid={key}"

        data = requests.get(url).json()
        # print(data)
        return data

    @ratelimit(key='ip', rate='10/m', block=True)
    @ratelimit(key='post:username', rate='5/m', method=['POST'])
    def authentication(request):
        # visitor_ip = request.META.get('HTTP_X_FORWARDED_FOR',
        #                               request.META.get('HTTP_X_REAL_IP', request.META.get('REMOTE_ADDR', None)))
        # ic(visitor_ip)
        # if request.COOKIES.get('is_limited') == "1":
        #     response = render(request, 'weather_app/403_error.html', status=429,
        #                       context={'status': 429, 'message': "Too Many Requests"})
        #     return response

        # response = redirect("Authentication")
        # if request.COOKIES.get("visited") is not None or str(request.COOKIES.get("visited")).lower() == "false" \
        #         or request.COOKIES.get("id_token") is not None or request.COOKIES.get('id_token'):
        #     response.delete_cookie("visited")
        #     response.delete_cookie("id_token")
        #     return response

        form = LoginForm()

        if request.method == 'POST':
            username = request.POST.get('username')
            password = request.POST.get('password')
            api = request.POST.get('api')
            user = authenticate(request, username=username, password=password)
            data = valid(api)
            response = redirect("index")
            max_age = 2 * 60 * 60

            if user is not None:
                print(data['cod'])
                if data['cod'] == 200:
                    login(request, user)
                    response.set_cookie("visited", True, max_age=max_age)
                    response.set_cookie("id_token", api, max_age=max_age, httponly=True)
                    print('Authenticated')
                else:
                    error_alert(request, data['message'])
            else:
                error_alert(request, "賬戶或密碼不正確")

            return response

        context = {
            'form': form
        }

        return render(request, 'authentication.html', context)

    def log_out(request):
        logout(request)
        response = redirect('Authentication')
        if request.COOKIES.get("visited") is not None or str(request.COOKIES.get("visited")).lower() == "false" \
                or request.COOKIES.get("id_token") is not None or request.COOKIES.get('id_token'):
            response.delete_cookie("visited")
            response.delete_cookie("id_token")

            return response

        return redirect('Authentication')

    def error_alert(request, message):
        messages.error(request, message)

    def handler403(request, exception=None):
        if isinstance(exception, Ratelimited):
            # return HttpResponse('Sorry you are blocked', status=429)
            context = {
                'status': 429,
                'message': "Too Many Requests."
            }
            log_out(request)
            response = render(request, 'weather_app/403_error.html', status=429, context=context)
            retry_after_seconds = 30
            retry_after_datetime = timezone.now() + timezone.timedelta(seconds=retry_after_seconds)
            response['Retry-After'] = retry_after_datetime.strftime('%a, %d %b %Y %H:%M:%S GMT')
            # response.set_cookie("is_limited", 1, expires=retry_after_datetime.strftime('%a, %d %b %Y %H:%M:%S GMT'))
            return response
            # return JsonResponse({'error': 'ratelimited'}, status=429)

        context = {
            'status': 403,
            'message': "Forbidden"
        }
        log_out(request)
        return render(request, '403_error.html', status=403, context=context)

except Exception as e:
    print(e)
