from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse, response, QueryDict,HttpResponseRedirect
from django.urls import reverse
from django.http.response import HttpResponseServerError
import firebase_admin
from firebase_admin import credentials, firestore
import boto3
from boto3.dynamodb.conditions import Attr, Key
from decimal import Decimal
import hashlib
import uuid
import smtplib
import json
from email.mime.text import MIMEText
from . import settings
from django.views.decorators.csrf import csrf_exempt
import requests
from geopy.distance import geodesic
from adminPanel import database
import os
from twilio.rest import Client
from datetime import date


# cred = credentials.Certificate('lifetime-software-firebase.json')
# firebase_admin.initialize_app(cred)
# db = firestore.client()

# db = boto3.resource(service_name = 'dynamodb',region_name = 'us-east-1',
#         aws_access_key_id = 'AKIAX3OUKCBBZKLTD3SH',
#         aws_secret_access_key = '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')

def index(request):
    userID=request.session.get('loginId')
    # carTypes=database.get_all_item('vehicleCategory')
    print(userID)
    if (userID == None):
        return render(request,'index.html',{'carTypes':[]})
    else:
        # userData= db.Table('users').get_item(Key={'userID':userID})['Item']
        return render(request,'index.html',{'carTypes':[]})





def contactUs(request):
    userID=request.session.get('loginId')
    if (userID == None):
        return render(request,'contactUs.html')
    else:
        # userData= db.Table('users').get_item(Key={'userID':userID})['Item']
        return render(request,'contactUs.html',{'userData':userData})


def aboutUs(request):
    userID=request.session.get('loginId')
    if (userID == None):
        return render(request,'aboutUs.html',)
    else:
        # userData= db.Table('users').get_item(Key={'userID':userID})['Item']
        return render(request, 'aboutUs.html',{'userData':userData})


def faqs(request):
    userID=request.session.get('loginId')
    if (userID == None):
        return render(request,'faq.html')
    else:
        # userData= db.Table('users').get_item(Key={'userID':userID})['Item']
        return render(request,'faq.html',{'userData':userData})


def logoutUser(request):
    del request.session['userID']
    if request.session.get('userType') != None:
        del request.session['userType']
    request.session.modified = True
    return JsonResponse({'status':'success'})
def login(request):
    return render(request,'login.html')


def confirmBooking(request):
    userID=request.session.get('loginId')
    if (userID == None):
        return render(request, 'login.html')
    else:
        # userData= db.Table('users').get_item(Key={'userID':userID})['Item']
        return render(request, 'confirmBooking.html',{'userData':userData})


def allBookings(request):
    userID=request.session.get('loginId')
    if (userID == None):
        return render(request, 'login.html')
    else:
        # userData= db.Table('users').get_item(Key={'userID':userID})['Item']
        return render(request,'allBookings.html',{'userData':userData})



def userProfile(request):
    userID=request.session.get('loginId')
    if (userID == None):
        return render(request, 'login.html')
    else:
        # userData= db.Table('users').get_item(Key={'userID':userID})['Item']
        allOrders=[]
        orderList=userData['orderList']
        for each in orderList:
            orderData=database.get_item('orders',each)
            allOrders.append(orderData)
        return render(request,'userProfile.html',{'userData':userData,'allOrders':allOrders})

def giveuserData(request):
    userID=request.session.get('loginId')
    # userData= db.Table('users').get_item(Key={'userID':userID})['Item']
    return userData


# =* LOG IN USER / ADD USER DATA
def addUserData(request):
    try:
        print('trying adding')
        receivedData = json.loads(str(request.body, encoding='utf-8'))
        try:
            print('existing user')
            userData = db.Table('users').get_item(Key={'userID':receivedData['userID']})['Item']
            request.session['loginId']=receivedData['userID']
            return JsonResponse({"status":"success"})
        except:
            try:
                print('new user')
                request.session['loginId']=receivedData['userID']
                receivedData["orderList"]=[]
                db.Table('users').put_item(Item=receivedData)
                return JsonResponse({"status":"success"})
            except Exception as e:
                return JsonResponse({"status":"failied2","error":e  })
    except Exception as e:
        print('not logged in')

        return JsonResponse({"status":"failied","error":e})


# =* LOG OUT
def logout(request):
    del request.session['loginId']
    return redirect('/')




def currentBooking(request):
    allData=receivedData = json.loads(str(request.body, encoding='utf-8'))
    print(allData)
    db.Table('users').update_item(
    Key={'userID':request.session.get('loginId')},
    UpdateExpression='SET bookingDetails = :changedbookingDetails',
    ExpressionAttributeValues={
    ':changedbookingDetails':allData,
    }
    )


    return JsonResponse({'status':'success'})



def choosePrice(request):
    userData=giveuserData(request)
    vehicleTypeId=userData['bookingDetails']['vehicleTypeId']

    # vehicleTypeData=database.get_item('vehicleCategory',vehicleTypeId)
    pickUpLocationCode={'lat':userData['bookingDetails']['pickUpLocation']['lat'],'lon':userData['bookingDetails']['pickUpLocation']['lon']}
    destinationLocationCode={'lat':userData['bookingDetails']['destinationLocation']['lat'],'lon':userData['bookingDetails']['destinationLocation']['lon']}

    origin = (float(pickUpLocationCode['lat']),float(pickUpLocationCode['lon']))
    dist = (float(destinationLocationCode['lat']),float(destinationLocationCode['lon']))
    totalDistance=int(geodesic(origin, dist).kilometers)
    totalPrice=(totalDistance*8)  + (totalDistance*6)
    # day driver allowance comes from per km driver charge from driver table
    # fuel charge
    # CALCULATE PRICE - per km charge * total distance + driver allowance per km * total distance + ac charger per km * total distance
    vehicleList=[]

    # db.Table('users').update_item(
    # Key={'userID':userData['userID']},
    # UpdateExpression='SET totalTripPrice = :newtotalTripPrice, totalDistance = :newtotalDistance ',
    # ExpressionAttributeValues={
    # ':newtotalTripPrice':str(totalPrice),
    # ':newtotalDistance':totalDistance
    # }
    # )


    return render(request,'choosePrice.html',{'userData':userData,'totalDistance':totalDistance,'totalPrice':totalPrice,})


account_sid = "AC0b484c1ca305d3820ac6ceb619e3f5b9"
auth_token = "55b373b918b3e09933f94af8fe5cf34e"
verify_sid = "VA7ed221e2e0bfc457c064459cd5efc2e9"
client = Client(account_sid, auth_token)

def sendOTP(request):
    receivedData = json.loads(str(request.body, encoding='utf-8'))
    print(receivedData)
    userPhoneNumber= str(receivedData['OTPnumber'])
    verified_number = f"+91{userPhoneNumber}"
    request.session['verificationNumber']=verified_number
    print(type(verified_number))
    verification = client.verify.v2.services(verify_sid) \
    .verifications \
    .create(to=verified_number, channel="sms")
    print(verification.status)
    return JsonResponse({'status':'success'})




def verifyOTP(request):
    receivedData = json.loads(str(request.body, encoding='utf-8'))
    print(receivedData)
    otp_code=str(receivedData['OTP'])
    print(request.session['verificationNumber'])
    verified_number=str(request.session['verificationNumber'])

    verification_check = client.verify.v2.services(verify_sid) \
    .verification_checks \
    .create(to=verified_number, code=otp_code)
    if(verification_check.status == 'approved'):
        return JsonResponse({'status':'success'})
    else:
        return JsonResponse({'status':'failed'})

import random

def chooseCar(request):
    userData=giveuserData(request)
    vehicleId=userData['bookingDetails']['vehicleTypeId']
    # allCars=database.getDataOfSameType('cars','vehicleType-index','vehicleType',vehicleId)
    bookingConfirmationCode=''.join([str(random.randint(0,9)) for a in range(0,4)])
    print(bookingConfirmationCode)
    return render(request,'chooseACar.html',{'bookingConfirmationCode':bookingConfirmationCode,'userData':userData})


def orderConfirmation(request):
    receivedData = json.loads(str(request.body, encoding='utf-8'))
    userData=giveuserData(request)
    confirmationCode=receivedData['bookingConfirmationCode']
    vehicleId=receivedData['vehicleId']
    # vehicleData=database.get_item('cars',vehicleId)
    custEmail=receivedData['customerEmail']


    # server = smtplib.SMTP_SSL('smtp.zoho.in', 465)
    # server.login('noreply@grazzecabs.com', 'Sep2001#@')
    # data = f'<div style="text-align:left;width:100%;margin:0 auto"><p>Your order confirmation code : {confirmationCode}</p>Trip Details : <p>Vehicle Name : {vehicleData["vehicleName"]}</p><p>Vehicle Number : {vehicleData["vehicleNumber"]}</p><p>Total Trip Price : {userData["totalTripPrice"]}</p><p>Pick up location : {userData["bookingDetails"]["pickUpLocation"]["formattedName"]}</p><p>Destination Location  : {userData["bookingDetails"]["destinationLocation"]["formattedName"]}</p></div>'
    # msg = MIMEText(str(data), 'html')
    # recipients = [custEmail]
    # msg['Subject'] = "Email Verification"
    # msg['From'] = "noreply@grazzecabs.com"
    # msg['To'] = ", ".join(recipients)
    # server.sendmail('noreply@grazzecabs.com',recipients, msg.as_string())
    # server.close()

    # orderId=str(uuid.uuid4().hex)
    # orderData={
    #     'docId':orderId,
    #     'userData':userData,
    #     'Date':str(date.today()),
    #     'orderStatus':'pending',
    #     'orderEmail':custEmail,
    #     'bookingConfirmationCode':confirmationCode,
    #     'bookingUserName':receivedData['bookingUserName'],
    #     'bookingUserPhone':receivedData['orderUserPhone'],
    #     'bookingUserAddress':receivedData['orderUserAddress'],
    #     'driverStatus':'Not Approved'
    # }
    # orderList=userData['orderList']
    # orderList.append(orderId)
    # db.Table('users').update_item(
    # Key={'userID':userData['userID']},
    # UpdateExpression='SET orderList = :neworderList',
    # ExpressionAttributeValues={
    # ':neworderList':orderList,
    # }
    # )
    # database.put_item('orders',orderData)
    return JsonResponse({'status':'success'})





def thankyou(request):
    userData=giveuserData(request)
    # orderData=database.get_item('orders',orderId)
    return render(request,'thankyou.html',{'userData':userData})

def orderDetails(request):
    return render(request,'allBookings.html')



def updateUserProfile(request):
    receivedData = request.POST.dict()
    userId=request.session.get('loginId')
    print(receivedData)
    for each in receivedData:
        db.Table('users').update_item(
        Key={'userID':userId},
        UpdateExpression=f'SET {each} = :tempName',
        ExpressionAttributeValues={
        ':tempName':receivedData[each],
        }
        )

    return JsonResponse({'status':'success'})
