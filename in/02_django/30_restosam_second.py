{% section "Рестораны: вторая версия" %}

{% subsection "Странички сайта" %}
{% program "python" "restaurants/restaurants/" %}
from django.conf.urls import patterns, include, url

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

from django.contrib.auth.views import login, logout

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'restosam.views.home', name='home'),
    # url(r'^restosam/', include('restosam.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),

    url(r'^$', 'main_app.views.home'),

    url(r'^restaurants/([A-Za-z_-]+)/', 'main_app.views.restaurant'),

    url(r'^add_dish/', 'main_app.views.add_dish'),

    url(r'^login/', 'main_app.views.login', name='login'),

    url(r'^logout/$', logout, {'next_page': '/'}, name='logout'),

    url(r'^change_like/$', 'main_app.views.change_like'),
)
{% endprogram %}
{% endsubsection %}

{% subsection "Схема базы данных" %}
{% program "python" "restaurants/main_app/models.py" %}
from django.db import models


class Dish(models.Model):
	name = models.CharField(max_length=200)
	description = models.TextField()
	price = models.IntegerField()
	restaurant = models.ForeignKey('Restaurant', db_index=True)
	rating = models.IntegerField()


class Restaurant(models.Model):
	name = models.CharField(max_length=200) # Три сосны
	description = models.TextField(blank=True)
	urlname = models.CharField(max_length=200) # tri_sosny
	# urlname будет использоваться в адресной строке
	#     127.0.0.1:8000/restaurants/tri_sosny/

	# dish_set - неявное поле, создаётся из-за связи ForeignKey в Dish

	def __str__(self):
		return self.name	
{% endprogram %}
{% endsubsection %}

{% subsection "Настройка интерфейса администратора" %}
{% program "python" "restaurants/main_app/admin.py" %}
from django.contrib import admin
from main_app.models import Restaurant, Dish

admin.site.register(Restaurant)
admin.site.register(Dish)
{% endprogram %}
{% endsubsection %}

{% subsection "Определение форм" %}
{% program "python" "restaurants/main_app/forms.py" %}
from django import forms
from main_app.models import Restaurant

class DishAddForm(forms.Form):
    name = forms.CharField(label='Название блюда')
    description = forms.CharField(label='Описание блюда', widget=forms.Textarea, required=False)
    price = forms.IntegerField(label='Стоимость')
    restaurant = forms.ModelChoiceField(label='Ресторан', 
        queryset=Restaurant.objects.all())


class LoginForm(forms.Form):
	username = forms.CharField()
	password = forms.CharField()
{% endprogram %}
{% endsubsection %}

{% subsection "Обработчики запросов" %}
{% program "python" "restaurants/main_app/views.py" %}
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.contrib import auth

from main_app.models import Restaurant, Dish
from main_app.forms import DishAddForm, LoginForm

import json


def home(request):
	restaurants = Restaurant.objects.all()
	return render(request, 'main_template.html', locals())


def restaurant(request, group):
	r = Restaurant.objects.get(urlname=group)
	return render(request, 'restaurant.html', {'restaurant': r})


def add_dish(request):
	if request.user is not None:
	    if request.method == 'POST':
	        form = DishAddForm(request.POST)
	        if form.is_valid():
	            d = form.cleaned_data
	            new_dish = Dish(**d)
	            new_dish.save()
	            return HttpResponse('Спасибо, всё добавилось')
	        else:
	            return HttpResponse('Форма некорректна')
	    else:
	        form = DishAddForm()
	        return render(request, 'add_dish.html', {'form': form, 'request': request})
	else:
	    return HttpResponse('Вы не залогинены')


def login(request):
	if request.method == 'POST':
	    username = request.POST.get('username', '')
	    password = request.POST.get('password', '')
	    user = auth.authenticate(username=username, password=password)
	    if user is not None and user.is_active:
	        # Correct password, and the user is marked "active"
	        auth.login(request, user)
	        # Redirect to a success page.
	        return HttpResponseRedirect("/")
	    else:
	        # Show an error page
	        return HttpResponse('Не удалось залогиниться')
	else:
	    form = LoginForm()
	    return render(request, 'login.html', locals())


def change_like(request):
	# ajax post request
	dish_id = int(request.POST['dish_id'])
	diff = int(request.POST['diff'])
	dish = Dish.objects.get(id=dish_id)
	dish.rating += diff
	dish.save()
	data = {'dish_id': dish_id, 'rating': dish.rating}
	output_json = json.dumps({})
	return HttpResponse(output_json, mimetype='text/plain') 
{% endprogram %}
{% endsubsection %}

{% subsection "Шаблоны страниц" %}
{% program "django" "restaurants/templates/base.html" %}
<html>
<head>
<script type="text/javascript" src="http://code.jquery.com/jquery-1.9.1.min.js"></script>
{% block additional_head %}

{% endblock %}
</head>
<body>
{% if request.user.is_authenticated %}
Вы вошли как {{ user }}. <a href="{% url 'login' %}">Выйти</a>
{% else %}
Вы не залогинены. <a href="{% url 'logout' %}">Залогиниться</a>
{% endif %}
<hr>
{% block body %}
{% endblock %}
</body>
</html>
{% endprogram %}

{% program "python" "restaurants/templates/main_template.html" %}
{% endprogram %}

{% program "python" "restaurants/templates/restaurants.html" %}
{% endprogram %}

{% program "python" "restaurants/templates/login.html" %}
{% endprogram %}

{% program "python" "restaurants/templates/add_dish.html" %}
{% endprogram %}
{% endsubsection %}

{% endsection %}