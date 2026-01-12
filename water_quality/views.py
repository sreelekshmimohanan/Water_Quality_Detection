from django.http import HttpResponse
from django.shortcuts import render
from django.shortcuts import redirect
# FILE UPLOAD AND VIEW
from  django.core.files.storage import FileSystemStorage
# SESSION
from django.conf import settings
from .models import *
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'ML'))
from inference import predict_potability

def first(request):
    return render(request,'index.html')
def index(request):
    return render(request,'index.html')
def addreg(request):
    if request.method=="POST":
        a=request.POST.get('name')
        b=request.POST.get('phone_number')
        c=request.POST.get('email')
        d=request.POST.get('password')
        e=regtable(name=a,phone_number=b,email=c,password=d)
        e.save()
    return render(request,'index.html')

def register(request):
    return render(request,'register.html')

def staff_register(request):
    return render(request,'staff_register.html')

def add_staff_reg(request):
    if request.method=="POST":
        a=request.POST.get('name')
        b=request.POST.get('phone_number')
        c=request.POST.get('email')
        d=request.POST.get('password')
        e=Staff(name=a,phone_number=b,email=c,password=d)
        e.save()
    return render(request,'index.html')

def login(request):
    return render(request,'login.html')

def addlogin(request):
    email = request.POST.get('email')
    password = request.POST.get('password')
    if email == 'admin@gmail.com' and password =='admin':
        request.session['admin'] = 'admin'
        return render(request,'index.html')

    elif regtable.objects.filter(email=email,password=password).exists():
            userdetails=regtable.objects.get(email=request.POST['email'], password=password)
            request.session['uid'] = userdetails.id
            request.session['role'] = 'user'
            return render(request,'index.html')

    elif Staff.objects.filter(email=email,password=password).exists():
            staffdetails=Staff.objects.get(email=request.POST['email'], password=password)
            request.session['sid'] = staffdetails.id
            request.session['role'] = 'staff'
            return render(request,'index.html')

    else:
        return render(request, 'index.html', {'message':'Invalid Email or Password'})
    



def viewusers(request):
    user=regtable.objects.all()
    return render(request,'viewusers.html',{'result':user})





def profile(request):
    uid = request.session.get('uid')
    if not uid:
        return redirect(login)
    try:
        user = regtable.objects.get(id=uid)
    except regtable.DoesNotExist:
        return redirect(login)
    return render(request, 'profile.html', {'user': user})

def prediction_history(request):
    uid = request.session.get('uid')
    if not uid:
        return redirect(login)
    predictions = Prediction.objects.filter(user_id=uid).order_by('-created_at')
    return render(request, 'prediction_history.html', {'predictions': predictions})

def staff_profile(request):
    sid = request.session.get('sid')
    if not sid:
        return redirect(login)
    try:
        staff = Staff.objects.get(id=sid)
    except Staff.DoesNotExist:
        return redirect(login)
    return render(request, 'staff_profile.html', {'staff': staff})

def view_predictions(request):
    sid = request.session.get('sid')
    if not sid:
        return redirect(login)
    predictions = Prediction.objects.all().select_related('user').order_by('-created_at')
    return render(request, 'view_predictions.html', {'predictions': predictions})

def add_feedback(request):
    if request.method == 'POST':
        subject = request.POST.get('subject')
        message = request.POST.get('message')
        uid = request.session.get('uid')
        sid = request.session.get('sid')
        if uid:
            user = regtable.objects.get(id=uid)
            Feedback.objects.create(user=user, subject=subject, message=message)
        elif sid:
            staff = Staff.objects.get(id=sid)
            Feedback.objects.create(staff=staff, subject=subject, message=message)
        return redirect('index')
    return render(request, 'add_feedback.html')

def view_feedback(request):
    if not (request.session.get('sid') or request.session.get('admin')):
        return redirect(login)
    feedbacks = Feedback.objects.all().select_related('user', 'staff').order_by('-created_at')
    return render(request, 'view_feedback.html', {'feedbacks': feedbacks})

def predict_potability_view(request):
    uid = request.session.get('uid')
    if not uid:
        return redirect(login)
    if request.method == 'POST':
        # Get form data
        data = {
            'ph': float(request.POST.get('ph')),
            'Hardness': float(request.POST.get('Hardness')),
            'Solids': float(request.POST.get('Solids')),
            'Chloramines': float(request.POST.get('Chloramines')),
            'Sulfate': float(request.POST.get('Sulfate')),
            'Conductivity': float(request.POST.get('Conductivity')),
            'Organic_carbon': float(request.POST.get('Organic_carbon')),
            'Trihalomethanes': float(request.POST.get('Trihalomethanes')),
            'Turbidity': float(request.POST.get('Turbidity'))
        }
        # Predict
        prediction = predict_potability(data)
        result = 'Potable' if prediction == 1 else 'Not Potable'
        
        # Save to database
        uid = request.session.get('uid')
        if uid:
            user = regtable.objects.get(id=uid)
            Prediction.objects.create(
                user=user,
                ph=data['ph'],
                Hardness=data['Hardness'],
                Solids=data['Solids'],
                Chloramines=data['Chloramines'],
                Sulfate=data['Sulfate'],
                Conductivity=data['Conductivity'],
                Organic_carbon=data['Organic_carbon'],
                Trihalomethanes=data['Trihalomethanes'],
                Turbidity=data['Turbidity'],
                result=result
            )
        
        return render(request, 'predict_potability.html', {'result': result, 'data': data})
    return render(request, 'predict_potability.html')

def logout(request):
    session_keys = list(request.session.keys())
    for key in session_keys:
        del request.session[key]
    return redirect(first)