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
from . import database
# from . import settings
from django.views.decorators.csrf import csrf_exempt
db = boto3.resource(service_name = 'dynamodb',region_name = 'us-east-1',
        aws_access_key_id = 'AKIAX3OUKCBBZKLTD3SH',
        aws_secret_access_key = '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')


def index(request):
    if request.session.get('adminLogin'):
        return render(request, 'adminPanel/adminHome.html')
    else:
        return render(request, 'adminPanel/adminLogin.html')

def recentOrders(request):
    allOrders=database.get_all_item('orders')
    allDrivers=database.get_all_item('drivers')
    if request.session.get('adminLogin'):
        return render(request, 'adminPanel/recentOrder.html',{'allOrders':allOrders,'allDrivers':allDrivers})
    else:
        return render(request, 'adminPanel/adminLogin.html')

def addVehicle(request):
    vehicleTypes=database.get_all_item('vehicleCategory')
    if request.session.get('adminLogin'):
        return render(request, 'adminPanel/addVehicle.html',{'vehicleTypes':vehicleTypes})
    else:
        return render(request, 'adminPanel/adminLogin.html')

def allVehicle(request):
    allVehicles=database.get_all_item('cars')
    if request.session.get('adminLogin'):
        return render(request, 'adminPanel/allVehicle.html',{'allVehicles':allVehicles})
    else:
        return render(request, 'adminPanel/adminLogin.html')

def addDriver(request):
    if request.session.get('adminLogin'):
        return render(request, 'adminPanel/addDriver.html')
    else:
        return render(request, 'adminPanel/adminLogin.html')

def allDriver(request):
    allDrivers=database.get_all_item('drivers')
    if request.session.get('adminLogin'):
        return render(request, 'adminPanel/allDriver.html',{'allDrivers':allDrivers})
    else:
        return render(request, 'adminPanel/adminLogin.html')

def adminLogin(request):
    return render(request, 'adminPanel/adminLogin.html')

def errorPage(request):
    return render(request,'adminPanel/errorPage.html')

def vehicleCategory(request):
    return render(request,'adminPanel/vehicleCategory.html')


def addNewCategory(request):
    receivedData = request.POST.dict()
    allFiles=request.FILES.dict()
    docId=uuid.uuid4().hex
    receivedData['docId']=docId
    storedLocation=database.put_image('vehicleCategoryImage',allFiles,docId)
    receivedData.update(storedLocation)
    db.Table('vehicleCategory').put_item(Item=receivedData)

    return JsonResponse({'status':'success'})
    


def addNewVehicle(request):
    receivedData = request.POST.dict()
    allFiles=request.FILES.dict()
    docId=uuid.uuid4().hex
    receivedData['docId']=docId
    storedLocation=database.put_image('vehicleImages',allFiles,docId)
    receivedData.update(storedLocation)
    db.Table('cars').put_item(Item=receivedData)
    return JsonResponse({'status':'success'})
    



def addNewDriver(request):
    receivedData = request.POST.dict()
    allFiles=request.FILES.dict()
    docId=uuid.uuid4().hex
    receivedData['docId']=docId
    storedLocation=database.put_image('driverImage',allFiles,docId)
    receivedData.update(storedLocation)
    database.put_item('drivers',receivedData)
    return JsonResponse({'status':'success'})
    
    
def editVehicle(request,docId):
    vehicleData=database.get_item('cars',docId)
    vehicleTypes=database.get_all_item('vehicleCategory')
    for each in vehicleTypes:
        if each['docId']==vehicleData['vehicleType']:
            vehicleData['vehicleTypeName']=each['categoryName']
    return render(request,'adminPanel/editVehicle.html',{'vehicleData':vehicleData,'vehicleTypes':vehicleTypes})



def editSpecificVehicle(request):
    receivedData = request.POST.dict()
    allFiles=request.FILES.dict()
    vehicleId=receivedData['docId']
    del receivedData['docId']
    print(receivedData,allFiles,vehicleId)
    if allFiles:
        storedLocation=database.put_image('driverImage',allFiles,vehicleId)
        for each in storedLocation:
            receivedData[each]=storedLocation[each]

    if receivedData['vehicleType'] == 'none':
        del receivedData['vehicleType']
    
    for each in receivedData:
        db.Table('cars').update_item(
        Key={'docId':vehicleId},
        UpdateExpression=f'SET {each} = :tempName',
        ExpressionAttributeValues={
        ':tempName':receivedData[each],
        }
        )
    
    return JsonResponse({'status':'success'})
    


def assignDriver(request):
    receivedData = json.loads(str(request.body, encoding='utf-8'))
    orderData=database.get_item('orders',receivedData["orderId"])
    driverData=database.get_item('drivers',receivedData["selectedDriver"])
    

    # =$ EMAIL FOR USER
    custEmail=orderData['orderEmail']
    server = smtplib.SMTP_SSL('smtp.zoho.in', 465)
    server.login('noreply@grazzecabs.com', 'Sep2001#@')
    data = f'<div style="text-align:left;width:100%;margin:0 auto"><p>Driver for your trip : </p><p>Driver Name : {driverData["driverName"]}</p><p>Driver Contact Number : {driverData["driverContact"]}</p><p>Driver Email : {driverData["driverEmail"]}</p><p>Booking Confirmation code {orderData["bookingConfirmationCode"]} please share the code with your Delivery person.</p></div>'
    msg = MIMEText(str(data), 'html')
    recipients = [custEmail]
    msg['Subject'] = "Email Verification"   
    msg['From'] = "noreply@grazzecabs.com"
    msg['To'] = ", ".join(recipients)
    server.sendmail('noreply@grazzecabs.com',recipients, msg.as_string())
    server.close()


    # =$ EMAIL FOR DRIVER
    driverEmail=driverData['driverEmail']
    server = smtplib.SMTP_SSL('smtp.zoho.in', 465)
    server.login('noreply@grazzecabs.com', 'Sep2001#@')
    data = f'<div style="text-align:left;width:100%;margin:0 auto"><p>You are assigned for a trip.<p>Trip details : </p></p><p>User Name : {orderData["userData"]["userName"]}</p><p>User email : {orderData["orderEmail"]}</p><p>Your order confirmation code : {orderData["bookingConfirmationCode"]}</p>Trip Details : <p>Total Trip Price : {orderData["userData"]["totalTripPrice"]}</p><p>Pick up location : {orderData["userData"]["bookingDetails"]["pickUpLocation"]["formattedName"]}</p><p>Destination Location  : {orderData["userData"]["bookingDetails"]["destinationLocation"]["formattedName"]}</p></div>'
    msg = MIMEText(str(data), 'html')
    recipients = [driverEmail]
    msg['Subject'] = "Email Verification"   
    msg['From'] = "noreply@grazzecabs.com"
    msg['To'] = ", ".join(recipients)
    server.sendmail('noreply@grazzecabs.com',recipients, msg.as_string())
    server.close()




    db.Table('orders').update_item(
    Key={'docId':receivedData["orderId"]},
    UpdateExpression='SET assignedDriver = :newassignedDriver, driverStatus = :newstatus',
    ExpressionAttributeValues={
    ':newassignedDriver':receivedData["selectedDriver"],
    ':newstatus':'Assigned'
    }
    )
    

    return JsonResponse({'status':'success'})
    



def adminLoginFetch(request):
    receivedData = json.loads(str(request.body, encoding='utf-8'))
    try:
        adminData=database.get_item('admin',receivedData['adminEmail'])
        if adminData['password'] == receivedData['adminPassword']:
            request.session['adminLogin']=adminData['docId']
            return JsonResponse({'status':'success'})
        else:
            return JsonResponse({'status':'failed2'})
    except:
        return JsonResponse({'status':'failed1'})
        

    print(adminData)
    return JsonResponse({'status':'success'})
    
