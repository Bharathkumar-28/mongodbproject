from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required

from .forms import registerform

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

def chat(request):
    """Handles chat messages sent from the frontend."""
    if request.method == 'POST':
        user_message = request.POST.get('message', '').strip()
        
        if not user_message:
            return JsonResponse({"reply": "Please enter a valid message."}, status=400)
        
        # Create a new chat session with the provided message
        chat_session = model.start_chat(history=history)
        response = chat_session.send_message(user_message)
        
        # Capture the response text
        model_response = response.text
        
        # Append the user and model messages to the history
        history.append({"role": "user", "parts": [user_message]})
        history.append({"role": "model", "parts": [model_response]})
        
        # Return the model's response as JSON
        return JsonResponse({"reply": model_response})

 
    return JsonResponse({"reply": "Invalid request."}, status=400)
from django.shortcuts import render
from .forms import ResumeForm
from django.http import FileResponse
from io import BytesIO
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from pymongo import MongoClient

client = MongoClient('mongodb://localhost:27017/')
db = client['resumedb']
collection = db['resumes']

def resume_form(request):
    if request.method == 'POST':
        form = ResumeForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            collection.insert_one(data)  # Save to MongoDB

            # Generate PDF
            buffer = BytesIO()
            p = canvas.Canvas(buffer, pagesize=A4)
            p.setFont("Helvetica-Bold", 16)
            p.drawString(100, 800, f"Resume - {data['name']}")
            
            p.setFont("Helvetica", 12)
            p.drawString(100, 770, f"Email: {data['email']}")
            p.drawString(100, 750, f"Phone: {data['phone']}")

            p.setFont("Helvetica-Bold", 14)
            p.drawString(100, 720, "Skills:")
            p.setFont("Helvetica", 12)
            for i, line in enumerate(data['skills'].split('\n')):
                p.drawString(120, 700 - i*15, f"- {line.strip()}")

            p.setFont("Helvetica-Bold", 14)
            p.drawString(100, 640, "Experience:")
            p.setFont("Helvetica", 12)
            for i, line in enumerate(data['experience'].split('\n')):
                p.drawString(120, 620 - i*15, f"- {line.strip()}")

            p.setFont("Helvetica-Bold", 14)
            p.drawString(100, 560, "Internships:")
            p.setFont("Helvetica", 12)
            for i, line in enumerate(data['internships'].split('\n')):
                p.drawString(120, 540 - i*15, f"- {line.strip()}")

            p.showPage()
            p.save()
            buffer.seek(0)
            return FileResponse(buffer, as_attachment=True, filename='resume.pdf')
    else:
        form = ResumeForm()

    return render(request, 'resume_form.html', {'form': form})
