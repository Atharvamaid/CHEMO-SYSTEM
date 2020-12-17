from django.shortcuts import render, HttpResponse, redirect
import pyrebase, requests
from time import time
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate,logout, login
from random_username.generate import generate_username

# Create your views h
from django.contrib.auth.views import PasswordChangeView
from plotly.offline import plot
from plotly.graph_objs import Scatter

config = {
  'apiKey': "AIzaSyDDmBnv6lOU3ANBvq0H7D8BOh-yxQVcZmI",
  'authDomain': "local-chemo-system.firebaseapp.com",
  'databaseURL' : 'https://local-chemo-system-default-rtdb.firebaseio.com/',
  'projectId': "local-chemo-system",
  'storageBucket': "local-chemo-system.appspot.com",
  'messagingSenderId': "839736070372",
  'appId': "1:839736070372:web:bbc24f1c631a6e1db05cf1",
  'measurementId': "G-5B8NBJ8955"
  }

firebase = pyrebase.initialize_app(config)

def Home(request):
  if request.user.is_authenticated:
    if request.user.last_name=='supplier':
      return redirect('supplier_dashboard')
    else:
      return redirect('dashboard')
  else:
    return render(request, 'hospitalauth/index.html')





def log_in(request):
  if request.user.is_authenticated:
    return redirect('Home')
  else:
    if request.method == 'POST':
      try:
        username = User.objects.get(email=request.POST['email']).username
        password = request.POST['pass']
        user = authenticate(request, username=username, password=password)
        if user:
          login(request, user)
          return redirect('dashboard')
        else:
          messages.warning(request, 'Invalid email or password ! Try again')
      except User.DoesNotExist:
        user = None
        messages.warning(request, 'Invalid email or password ! Try again')
    return render(request, 'hospitalauth/login.html')


@login_required(login_url='login')
def TrackCases(request):

  db = firebase.database()

  name = db.child('Hospitals').child(request.user.id).child('Hospital_Name').get()
  address = db.child("Hospitals").child(request.user.id).child("Address").get()
  city = db.child('Hospitals').child(request.user.id).child("city").get()


  return render(request, 'hospitalauth/trackcases.html', {'name': name, "address": address, 'city':city})


@login_required(login_url='login')
def dashboard(request):
  db = firebase.database()

  name = db.child('Hospitals').child(request.user.id).child('Hospital_Name').get()
  address = db.child("Hospitals").child(request.user.id).child("Address").get()
  city = db.child('Hospitals').child(request.user.id).child("city").get()

  supplies = db.child("Hospitals").child(request.user.id).child("supplies").get()
  return render(request, 'hospitalauth/dashboard.html', {'name': name, "address": address, "supplies": supplies, 'city':city})


def Search(request):
  if request.method == 'POST':
    db = firebase.database()

    name = db.child('Hospitals').child(request.user.id).child('Hospital_Name').get()
    address = db.child("Hospitals").child(request.user.id).child("Address").get()
    search = request.POST['q']
    try:
      supplier_id = User.objects.get(first_name=search).id
      supplier = db.child("suppliers").child(supplier_id).get()
      messages.success(request, f'results found for {search} !')
    except User.DoesNotExist:
      messages.warning(request, 'results not found')

  return render(request, 'hospitalauth/search.html',
                {"supplier": supplier, "name": name, "address": address, "id": supplier_id})


def chat(request, name):
  print(name)
  db = firebase.database()
  name1 = name.split('-')
  name1 = " ".join(name1)
  name1 = name1.title()
  name = db.child('Hospitals').child(request.user.id).child('Hospital_Name').get()
  address = db.child("Hospitals").child(request.user.id).child("Address").get()
  city = db.child('Hospitals').child(request.user.id).child("city").get()


  supplierid = User.objects.get(first_name=name1).id

  chats = db.child('suppliers').child(supplierid).child('chats').child(request.user.first_name).get()

  mychats = db.child('Hospitals').child(request.user.id).child('chats').child(name1).get()

  if mychats.val()==None or chats.val()==None:
    return render(request, 'hospitalauth/chat.html',
                  {'name': name, 'name1': name1, 'address': address, 'city': city, 'chats': chats,
                   'mychats': mychats, })
  else:
    allchats = zip(mychats.each(), chats.each())
    for i in allchats:
      print(i[1].val()['time'])
    return render(request, 'hospitalauth/chat.html',
                  {'name': name, 'name1': name1, 'address': address, 'city': city, 'chats': chats,
                   'mychats': mychats, })




def send_message(request, name):
  name = name.split('-')
  name = " ".join(name)
  name = name.title()
  if request.method=='POST':
    db = firebase.database()
    db.child("Hospitals").child(request.user.id).child("chats").child(name).push({'content':request.POST['message'], "time":time()})
    print(time().as_integer_ratio())

  return HttpResponse('done')

def CreateAccount(request):
  dats = {
    'inpatients': {
      'confirmed': 0,
      'under_observation': 0,
      'total': 0
    },
    'Beds': {
      'available': 0,
      'occupied': 0,
      'total': 0
    },
    'staff': {
      'oncall': 0,
      'onshift': 0,
      'total': 0
    },
    'ventilators': {
      'available': 0,
      'in_use': 0,
      'total': 0
    },
    'surgical_masks': {
      'available': 0,
      'in_use': 0,
      'total': 0
    },
    'gloves': {
      'small': 0,
      'large': 0,
      'total': 0
    },
    'face_shield': {
      'available': 0,
      'in_use': 0,
      'total': 0
    },
    'isolation_gowns': {
      'small': 0,
      'large': 0,
      'total': 0
    },
    'respirators': {
      'N95': 0,
      'PAPR': 0,
      'total': 0
    }

  }
  if request.method == 'POST':
    name = request.POST['hosname']

    username = generate_username(1)
    email = request.POST['email']
    address = request.POST['address']
    district = request.POST['dist']
    city = request.POST['city']
    if name.isalnum()==False or address.isalnum()==False or city.isalnum()==False or district.isalnum()==False:
      if name.isspace() or address.isspace() or city.isspace() or district.isspace():
        messages.warning(request, 'please enter valid information')
      else:
        if request.POST['pass'] == request.POST['confpass']:
          try:
            useremail = User.objects.get(email=email)
            messages.warning(request, 'This email is already registered !')
          except User.DoesNotExist:
            password = request.POST['pass']
            user = User.objects.create_user(username=username[0], email=email, password=password, first_name=name,
                                            last_name='hospital')
            if user:
              messages.success(request, f'Account Created for {name}')
              data = dats
              db = firebase.database()
              db.child('Hospitals').child(user.id).set(
                {"Hospital_Name": name, "Address": address, "city": city, 'district': district})
              db.child("Hospitals").child(user.id).child("supplies").set(data)
              login(request, user)
              return redirect('dashboard')
            else:
              messages.warning(request, 'Account not created try again')
        else:
          messages.warning(request, "passwords didn't match ! Try again")
          return redirect('signup')
    else:
      messages.warning(request, 'Please provide valid information ! Fields must be text')





  return render(request, 'hospitalauth/signup.html')

def create_supplier_account(request):
  dat = {
    'Beds' : 'No',
    'ventilators': 'No',
    'surgical_masks': 'No',
    'gloves': 'No',
    'face_shield': 'No',
    'isolation_gowns': 'No',
    'respirators': 'No'
  }
  supname = request.POST['supname']
  supusername = generate_username(1)
  supemail = request.POST['supemail']
  supaddress = request.POST.get('supaddress')
  supdist = request.POST['supdist']
  suppass = request.POST['suppass']
  supcity = request.POST['supcity']
  if supname.isalnum() == False or supaddress.isalnum() == False or supcity.isalnum() == False or supdist.isalnum() == False:
    if supname.isspace() or supaddress.isspace() or supcity.isspace() or supdist.isspace():
      messages.warning(request, 'Please enter valid imformation')
    else:
      if request.POST['suppass'] == request.POST['supconfpass']:
        try:
          useremail = User.objects.get(email=supemail)
          messages.warning(request, 'This email is already registered !')
          return redirect('signup')
        except User.DoesNotExist:
          supplier = User.objects.create_user(username=supusername[0], email=supemail, password=suppass,
                                              first_name=supname,
                                              last_name='supplier')
          if supplier:
            db = firebase.database()
            db.child('suppliers').child(supplier.id).set(
              {'Supplier_Name': supname, "city": supcity, 'Address': supaddress, 'district': supdist,
               'available_supplies': dat})
            print('accout created for supplier')
            login(request, supplier)
            messages.success(request, f'Account created for {supname} !')
          return redirect('supplier_dashboard')
      else:
        messages.warning(request, "Passwords didn't match ! Please try again")
        return redirect('signup')
  else:
    messages.warning(request, "Please provide valid information")
    return redirect('signup')



def supplier_login(request):
  if request.user.is_authenticated:
    return redirect('supplier_dashboard')
  else:
      try:
        username = User.objects.get(email=request.POST['supemail']).username
        password = request.POST['suppass']
        user = authenticate(request, username=username, password=password)
        if user:
          login(request, user)
          return redirect('supplier_dashboard')
        else:
          messages.warning(request, 'Invalid email or password ! Try again')
          return redirect('login')
      except User.DoesNotExist:
        user = None
        messages.warning(request, 'Invalid email or password ! Try again')
        return redirect('login')

def request_supplies(request):
  db = firebase.database()
  query = db.child("suppliers").get()
  name = db.child('Hospitals').child(request.user.id).child('Hospital_Name').get()
  address = db.child("Hospitals").child(request.user.id).child("Address").get()
  city = db.child('Hospitals').child(request.user.id).child("city").get()
  return render(request, 'hospitalauth/supplier_list.html', {'name':name, 'address':address, 'city':city, 'query':query})


def my_orders(request):
  db = firebase.database()

  name = db.child('Hospitals').child(request.user.id).child('Hospital_Name').get()
  address = db.child("Hospitals").child(request.user.id).child("Address").get()
  city = db.child('Hospitals').child(request.user.id).child("city").get()
  myorders = db.child('Hospitals').child(request.user.id).child('Placed_Order').get()

  return render(request, 'hospitalauth/my_orders.html', {'name':name, 'address':address, 'city':city, 'myorders':myorders})


def place_order(request, id):
  db = firebase.database()
  data = {}
  name = db.child('Hospitals').child(request.user.id).child('Hospital_Name').get()
  address = db.child("Hospitals").child(request.user.id).child("Address").get()
  city = db.child('Hospitals').child(request.user.id).child("city").get()
  supplier = db.child('suppliers').child(id).get()
  print(id)
  if request.method=='POST':

    for i,j in supplier.val()['available_supplies'].items():
      if j == 'yes':
        if request.POST[i] != "":
          data[i] = request.POST[i]

    supplier_name = User.objects.get(id=id).first_name
    data['order_status'] = 'Order Placed'
    db.child('Hospitals').child(request.user.id).child('Placed_Order').child(supplier_name).set(data)
    db.child('suppliers').child(id).child('orders_recieved').child(name.val()).set(data)
    messages.success(request, 'Orders placed successfully !')
    return redirect('myorders')
  return render(request, 'hospitalauth/place_order.html', {'name':name, 'address':address, 'city':city, 'supplier':supplier})


def update_data(request):
  fin = {
    'inpatients': {
      'confirmed': 0,
      'under_observation': 0,
      'total': 0
    },
    'Beds': {
      'available': 0,
      'occupied': 0,
      'total': 0
    },
    'staff': {
      'oncall': 0,
      'onshift': 0,
      'total': 0
    },
    'ventilators': {
      'available': 0,
      'in_use': 0,
      'total': 0
    },
    'surgical_masks': {
      'available': 0,
      'in_use': 0,
      'total': 0
    },
    'gloves': {
      'small': 0,
      'large': 0,
      'total': 0
    },
    'face_shield': {
      'available': 0,
      'in_use': 0,
      'total': 0
    },
    'isolation_gowns': {
      'small': 0,
      'large': 0,
      'total': 0
    },
    'respirators': {
      'N95': 0,
      'PAPR': 0,
      'total': 0
    }

  }

  try:

    db = firebase.database()

    for i, j in fin.items():
      for k in j.keys():
        j[k] = request.POST[i + k]
    db.child("Hospitals").child(request.user.id).child("supplies").update(fin)
  except:
    print("error")
  return HttpResponse("fomr submitted")


def log_out(request):
  messages.success(request, 'Logged out successfully')
  logout(request)
  return redirect('Home')
