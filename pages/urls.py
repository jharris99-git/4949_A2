# pages/urls.py
from django.urls import path
from .views import formPageView, aboutPageView, resultsPageView, formPost

urlpatterns = [
    path('', formPageView, name='form'),
    path('about/', aboutPageView, name='about'),
    path('formPost/', formPost, name='formPost'),
    path('results/<int:age>/<int:insured>/<int:premium>/<int:vintage>/<int:gen_f>/<int:gen_m>/<int:v_age_1_2>/'
         '<int:v_age_less_1>/<int:v_age_2_plus>/<int:v_damage_n>/<int:v_damage_y>', resultsPageView, name='results'),
]
