from django.contrib import admin
from django.urls import path, include
from . import views


urlpatterns = [
    # path('admin/', admin.site.urls),
    path('admin/', include('adminPanel.urls')),
    path('', views.index,name='index'),
    path('aboutUs', views.aboutUs,name='aboutUs'),
    path('faqs/', views.faqs,name='faqs'),
    path('login/', views.login,name='login'),
    path('choosePrice/', views.choosePrice, name='choosePrice'),
    path('chooseCar/', views.chooseCar, name='chooseCar'),
    path('orderDetails/',views.orderDetails,name='orderDetails'),
    path('updateUserProfile/',views.updateUserProfile,name='updateUserProfile'),
    path('confirmBooking/', views.confirmBooking, name ='confirmBooking'),
    path('addUserData/',views.addUserData,name='addUserData'),
    path('logout/',views.logout,name='logout'),
    path('currentBooking/',views.currentBooking,name='currentBooking'),
    path('choosePrice/',views.choosePrice,name='choosePrice'),
    path('sendOTP/',views.sendOTP,name='sendOTP'),
    path('verifyOTP/',views.verifyOTP,name='verifyOTP'),
    path('allBookings/', views.allBookings, name='allBookings'),
    path('userProfile/', views.userProfile, name = 'userProfile'),
    path('orderConfirmation/',views.orderConfirmation,name='orderConfirmation'),
    path('thankyou/',views.thankyou,name='thankyou'),
    
]
