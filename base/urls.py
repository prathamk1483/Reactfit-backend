
from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('reactfit/v001/setupuser/',views.setupUser),
    path("reactfit/v001/chat/",views.continueChat),
    path("reactfit/v001/addwaterintakelog/",views.addWaterIntakeLog),
    path("reactfit/v001/adddietlog/",views.addDietLog)
    
]
