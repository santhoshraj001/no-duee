from django.shortcuts import render,redirect
from django.contrib import messages
from . models import *
import random 
from django.db.models import Sum, Count
from django.db import connection
from django.core.mail import send_mail
from django.core.mail import EmailMessage
from django.conf import settings
from datetime import datetime, timedelta
from datetime import date 
import datetime
from .utils import encode_face, verify_face, gen_frames
import cv2


camera = cv2.VideoCapture(0)

from datetime import date, timedelta





def staff_login(request):
	
	if request.session.has_key('staff_id'):
		return render(request,'staff_dashboard.html',{})
	else:
		if request.method == 'POST':
			name=request.POST.get('username')
			pwd=request.POST.get('password')
			user_exist=Staff_Detail.objects.filter(username=name,password=pwd)
			if user_exist:
				request.session['staff_name']= request.POST.get('username')
				a = request.session['staff_name']
				sess = Staff_Detail.objects.only('id').get(username=a).id
				request.session['staff_id']= sess
				return redirect('staff_dashboard')
			else:
				messages.success(request,'Invalid username or Password')
		return render(request,'staff_login.html',{})
def staff_dashboard(request):
	if request.session.has_key('staff_id'):
		return render(request,'staff_dashboard.html',{})
	else:
		return render(request,'staff_login.html',{})
def staff_logout(request):
    try:
        del request.session['staff_id']
        del request.session['staff_name']
    except:
     pass
    return render(request, 'staff_login.html', {})
def student_details(request):
	if request.session.has_key('staff_id'):
		detail = Student_Detail.objects.all().order_by('-id')
		return render(request,'student_details.html',{'detail':detail})
	else:
		return render(request,'staff_login.html',{})
def all_stud(request):
	if request.session.has_key('staff_id'):
		detail = Student_Due.objects.all().order_by('-id')
		if request.method == 'POST':
			a = request.POST.get('search')
			row = Student_Due.objects.filter(student_id=a)
			return render(request,'all_stud.html',{'row':row})
		return render(request,'all_stud.html',{'detail':detail})
	else:
		return render(request,'staff_login.html',{})
from django.shortcuts import render, redirect
from django.contrib import messages
from .models import Staff_Detail, Alert_Detail
from django.core.mail import EmailMessage
from django.conf import settings

def send_msg(request, pk, amt):
    if request.session.has_key('staff_id'):
        if request.method == "POST":
            staff_id = request.session['staff_id']
            sid = Staff_Detail.objects.get(id=int(staff_id))
            msg_content = request.POST.get('msg')
            # Retrieve the recipient email. Adjust as needed if you want to use POST data.
            recipient_email = request.GET.get('email')
            
            # Create an alert record.
            alert = Alert_Detail.objects.create(
                staff_name=sid,
                student_id=pk,
                msg=msg_content,
                amount=amt
            )
            
            if alert:
                subject = "Due Reminder"
                html_body = f"""
                <html>
                  <body>
                    <p>Dear Student,</p>
                    <p>This is a reminder regarding your due payment. Please find the details below:</p>
                    <ul>
                      <li><strong>Student ID:</strong> {pk}</li>
                      <li><strong>Due Amount:</strong> {amt} Rs</li>
                    </ul>
                    <p><strong>Message:</strong><br>{msg_content}</p>
                    <p>Thank you,<br>{getattr(sid, 'staff_name', 'Your Staff')}</p>
                  </body>
                </html>
                """
                recipient_list = [recipient_email]
                email_from = settings.EMAIL_HOST_USER
                
                email = EmailMessage(subject, html_body, email_from, recipient_list)
                email.content_subtype = "html"  # Set the email content type to HTML
                email.send()
                messages.success(request, 'Due Reminder Mail Sent Successfully.')
        return render(request, 'send_msg.html', {})
    else:
        return render(request, 'staff_login.html', {})

def all_due(request):
	if request.session.has_key('user_id'):
		student_id = request.session['user_id']
		row = Student_Due.objects.filter(student_id=student_id)
		return render(request,'all_due.html',{'row':row})
	else:
		return render(request,'student_login.html',{})



def insert_student(request):
    if request.method == 'POST':
        # Extract data from POST
        student_name = request.POST.get('student_name')
        student_id = request.POST.get('student_id')
        email_id = request.POST.get('email_id')
        phone_number = request.POST.get('phone_number')
        dob = request.POST.get('dob')
        gender = request.POST.get('gender')
        degree = request.POST.get('degree')
        dept = request.POST.get('dept')
        address = request.POST.get('address')
        country = request.POST.get('country')
        state = request.POST.get('state')
        city = request.POST.get('city')
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        # Handle file upload (if provided)
        image = request.FILES.get('image')
        
        # Create a new Student_Detail instance
        student = Student_Detail(
            student_name=student_name,
            student_id=student_id,
            email_id=email_id,
            phone_number=phone_number,
            dob=dob,
            gender=gender,
            degree=degree,
            dept=dept,
            address=address,
            country=country,
            state=state,
            city=city,
            username=username,
            password=password,
            image=image,
            face_data=encode_face(camera)
        )
        student.save()
        
        # Redirect to a success page or another view
       	messages.success(request,'Register Successfully..')
       	return render(request, 'register.html')
    else:
        # Render the insert form template (e.g., insert_student.html)
        return render(request, 'register.html')

from django.http import StreamingHttpResponse


def video_feed(request):
    return StreamingHttpResponse(
        gen_frames(camera),
        content_type='multipart/x-mixed-replace; boundary=frame'
    )


def face_verification(request):
    if request.method == 'POST':
        student_id = request.POST.get('student_id')
        
        try:
            student = Student_Detail.objects.get(student_id=student_id)
        except Student_Detail.DoesNotExist:
            messages.error(request, "Student not found.")
            return redirect('face_verification')
        
        # Use the global camera instance for verification.
        if verify_face(camera, student.face_data):
            # Turn off the camera after successful face verification.
            camera.release()
            request.session['user_id'] = student.student_id
            messages.success(request, f"Login successful for {student.student_name}")
            return redirect('dashboard')
        else:
            messages.error(request, "Face verification failed.")
            return redirect('face_verification')
    
    return render(request, 'face_verification.html')


def dashboard(request):
	if request.session.has_key('user_id'):
		return render(request,'dashboard.html',{})
	else:
		return render(request,'face_verification.html',{})
def logout(request):
    try:
        del request.session['user_id']
    except:
     pass
    return render(request, 'face_verification.html', {})