from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('recentOrders/', views.recentOrders, name='recentOrders'),
    path('addVehicle/', views.addVehicle, name='addVehicle'),
    path('allVehicle/', views.allVehicle, name='allVehicle'),
    path('vehicleCategory/',views.vehicleCategory,name='vehicleCategory'),
    path('addNewCategory/',views.addNewCategory,name='addNewCategory'),
    # =$ ADD NEW VEHICLE FETCH FUNCTION
    path('addNewVehicle/',views.addNewVehicle,name='addNewVehicle'),
    path('addDriver/', views.addDriver, name='addDriver'),
    # =$ ADD NEW DRIVER FETCH FUNCTION
    path('addNewDriver/', views.addNewDriver, name='addDriver'),
    path('allDriver/', views.allDriver, name='allDriver'),
    path('adminLogin/', views.adminLogin, name='adminLogin'),
    path('errorPage/', views.errorPage, name='errorPage'),
    path('editVehicle/<str:docId>/',views.editVehicle,name='editVehicle'),
    path('editSpecificVehicle/',views.editSpecificVehicle,name='editSpecificVehicle'),
    path('assignDriver/',views.assignDriver,name='assignDriver'),
    path('adminLoginFetch/',views.adminLoginFetch,name='adminLoginFetch'),
    
    

]