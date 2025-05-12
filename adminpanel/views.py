from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required

from .forms import ResumeForm, registerform

from django.contrib.auth.models import Group
from django.contrib.auth.decorators import permission_required
from django.shortcuts import get_object_or_404, render,redirect
from django.http import HttpResponse
from django.urls import  reverse
from django.contrib import messages
from .forms import  registerform,loginform
from django.contrib.auth import authenticate,login as auth_login,logout as auth_logout
from django.contrib.auth.models import User
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_encode,urlsafe_base64_decode
from django.utils.encoding import force_bytes
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.core.mail import  send_mail
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator

import pdb
import logging
from django.http import JsonResponse

import json
from django.views.decorators.csrf import csrf_exempt
from django.core import serializers
from django.db.models import Count,Avg



def index(request):
    # Your view logic here
    return render(request, 'index.html')
def examples(request):
    # Your view logic here
    return render(request, 'example.html')
def register(request):
    if request.method == 'POST':
        form = registerform(request.POST)
        if form.is_valid():
            form.save()
            return redirect('index')  # Redirect to the index page after successful registration
    else:
        form = registerform()
    return render(request, 'register.html', {'form': form})


from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import loginform
 # Assuming you have a User model linked to MongoDB through djongo

def login(request):
    if request.session.get('username'):
        return redirect('/')

    form = loginform()
    if request.method == "POST":
        form = loginform(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username'].strip()
            password = form.cleaned_data['password'].strip()

            print(f"Username: {username}, Password: {password}")  # Debugging

            try:
                # Now, using Django ORM (djongo connects to MongoDB internally)
                user = User.objects.get(username=username)

                if user.password.strip() == password:
                    # Successful login
                    request.session['username'] = username
                    messages.success(request, 'You are successfully logged in')
                    return redirect('/')
                else:
                    messages.error(request, 'Incorrect password')

            except User.DoesNotExist:
                messages.error(request, 'Username does not exist')

        else:
            print("Form is not valid")  # Debugging
            print(form.errors)

    return render(request, "login.html", {'form': form})

            
            
from django.shortcuts import redirect

def logout(request):
    request.session.flush()  # Optional: clears entire session (recommended)
    return redirect('/')
   



# Create your views here.
from django.shortcuts import render
from django.http import JsonResponse
import google.generativeai as genai

# Configure Gemini
api_key = "AIzaSyBNBgchXs6MmOx-lBQSnovzCoyOuC18MY0"  # Replace with your actual API key
genai.configure(api_key=api_key)

# Set the generation configuration
generation_config = {
    "temperature": 1,
    "top_p": 0.95,
    "top_k": 40,
    "max_output_tokens": 8192,
    "response_mime_type": "text/plain",
}

# Initialize the Generative Model
model = genai.GenerativeModel(
    model_name="gemini-1.5-pro",
    generation_config=generation_config,
    system_instruction="Your dyslexia support instructions here...",
)

# Initial chat history
history = [
    {"role": "user", "parts": ["hi"]},
    {"role": "model", "parts": ["Hello! How can I assist you today? today you will some words and spell the words"]},
]

def home(request):
    
    return render(request, 'chatbot.html')
import fitz  # PyMuPDF
from django.core.files.uploadedfile import UploadedFile


from django.http import JsonResponse
from django.views.decorators.http import require_POST
@csrf_exempt
@require_POST
def chat(request):
    """Handles chat messages or resume uploads from the frontend."""

    # Handle resume upload
    if 'resume' in request.FILES:
        resume_file: UploadedFile = request.FILES['resume']
        if resume_file.content_type != 'application/pdf':
            return JsonResponse({"reply": "Only PDF files are accepted."}, status=400)

        try:
            # Read file content and extract text using PyMuPDF
            pdf_content = resume_file.read()
            doc = fitz.open(stream=pdf_content, filetype='pdf')
            extracted_text = ''
            for page in doc:
                extracted_text += page.get_text()

            # You can now "analyze" the resume
            # For example: check for skills, experience, etc.
            if "Python" in extracted_text:
                analysis = "Your resume mentions Python. Great choice!"
            else:
                analysis = "Consider adding Python if you know it — it's in demand."

            return JsonResponse({
                "reply": f"Resume analyzed.\n\nSummary:\n{analysis}"
            })

        except Exception as e:
            return JsonResponse({"reply": f"Failed to analyze resume: {str(e)}"}, status=500)

    # Handle chat messages
    user_message = request.POST.get('message', '').strip()

    if not user_message:
        return JsonResponse({"reply": "Please enter a valid message."}, status=400)

    try:
        chat_session = model.start_chat(history=history)
        response = chat_session.send_message(user_message)
        model_response = response.text

        history.append({"role": "user", "parts": [user_message]})
        history.append({"role": "model", "parts": [model_response]})

        return JsonResponse({"reply": model_response})
    
    except Exception as e:
        return JsonResponse({"reply": "An error occurred while processing your message."}, status=500)
def oii(request):
    return render(request, 'resume_form.html')    
from django.shortcuts import render, redirect
from .forms import ResumeForm
from .models import Resume

from django.shortcuts import render
from django.http import HttpResponse
from io import BytesIO
from reportlab.pdfgen import canvas
from .forms import ResumeForm
from .models import Resume

def resume_form(request):
    if request.method == 'POST':
        form = ResumeForm(request.POST)
        if form.is_valid():
            # Save to MongoDB
            resume = Resume(
                name=form.cleaned_data['name'],
                email=form.cleaned_data['email'],
                phone=form.cleaned_data['phone'],
                skills=form.cleaned_data['skills'],
                experience=form.cleaned_data['experience'],
                internships=form.cleaned_data['internships']
            )
            resume.save()

            # === PDF GENERATION ===
            buffer = BytesIO()
            p = canvas.Canvas(buffer)
            width, height = p._pagesize

            y = height - 50  # Start from top

            p.setFont("Helvetica-Bold", 16)
            p.drawString(100, y, "Professional Resume")
            y -= 30

            p.setFont("Helvetica", 12)
            p.drawString(100, y, f"Name: {resume.name}")
            y -= 20
            p.drawString(100, y, f"Email: {resume.email}")
            y -= 20
            p.drawString(100, y, f"Phone: {resume.phone}")
            y -= 30

            p.setFont("Helvetica-Bold", 14)
            p.drawString(100, y, "Skills:")
            y -= 20
            p.setFont("Helvetica", 12)
            for skill in resume.skills.split(','):
                p.drawString(120, y, f"- {skill.strip()}")
                y -= 15

            y -= 10
            p.setFont("Helvetica-Bold", 14)
            p.drawString(100, y, "Experience:")
            y -= 20
            p.setFont("Helvetica", 12)
            for line in resume.experience.split('\n'):
                p.drawString(120, y, line.strip())
                y -= 15

            if resume.internships.strip():
                y -= 10
                p.setFont("Helvetica-Bold", 14)
                p.drawString(100, y, "Internships:")
                y -= 20
                p.setFont("Helvetica", 12)
                for line in resume.internships.split('\n'):
                    p.drawString(120, y, line.strip())
                    y -= 15

            p.showPage()
            p.save()
            buffer.seek(0)

            return HttpResponse(buffer, content_type='application/pdf')

    else:
        form = ResumeForm()

    return render(request, 'resume_.html', {'form': form})

# views.py

from django.shortcuts import render, redirect
from .models import Resume
from bson import ObjectId  # Only if you're not using MongoEngine's default string ID
from django.views.decorators.csrf import csrf_exempt

def manage_resumes(request):
    if request.method == 'POST':
        action = request.POST.get('action')
        resume_id = request.POST.get('resume_id')

        if action == 'delete' and resume_id:
            resume = Resume.objects.filter(id=resume_id).first()
            if resume:
                resume.delete()
            return redirect('manage_resumes')

        elif action == 'update' and resume_id:
            resume = Resume.objects.filter(id=resume_id).first()
            if resume:
                resume.name = request.POST.get('name')
                resume.email = request.POST.get('email')
                resume.phone = request.POST.get('phone')
                resume.skills = request.POST.get('skills')
                resume.experience = request.POST.get('experience')
                resume.internships = request.POST.get('internships')
                resume.save()
            return redirect('manage_resumes')

    resumes = Resume.objects.all()  # ✅ Corrected here
    return render(request, 'resume_list.html', {'resumes': resumes})
