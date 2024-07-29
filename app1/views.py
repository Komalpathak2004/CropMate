from django.shortcuts import render, HttpResponse, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
import cv2
import os

@login_required(login_url='login')
def HomePage(request):
    result = None
    error_message = None
    if request.method == 'POST':
        seed_density = request.POST.get('density')
        file = request.FILES.get('image')

        if file and seed_density:
            # Check for valid file type
            if not file.name.lower().endswith(('.png', '.jpg', '.jpeg')):
                error_message = "Invalid file type. Please upload an image."
            else:
                # Handle file upload
                upload_path = os.path.join('uploads', file.name)
                with open(upload_path, 'wb+') as destination:
                    for chunk in file.chunks():
                        destination.write(chunk)

                # Calculate area and seed amount
                land_area = calculate_area(upload_path)
                if land_area <= 0:
                    error_message = "Could not calculate the area from the uploaded image."
                else:
                    seed_density = int(seed_density)
                    seed_amount = calculate_seed_amount(land_area, seed_density)
                    result = f"Total area of the land: {land_area:.2f} square meters<br>Approximate amount of seeds/plants needed: {seed_amount:.2f} seeds/plants"

                # Optionally remove the uploaded image after processing
                os.remove(upload_path)

    return render(request, 'home.html', {'result': result, 'error_message': error_message})

def SignupPage(request):
    if request.method == 'POST':
        uname = request.POST.get('username')
        email = request.POST.get('email')
        pass1 = request.POST.get('password1')
        pass2 = request.POST.get('password2')

        if pass1 != pass2:
            return HttpResponse("Your password and confirm password are not the same!")
        else:
            my_user = User.objects.create_user(uname, email, pass1)
            my_user.save()
            return redirect('login')

    return render(request, 'signup.html')

def LoginPage(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        pass1 = request.POST.get('pass')
        user = authenticate(request, username=username, password=pass1)
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            return HttpResponse("Username or Password is incorrect!")

    return render(request, 'login.html')

def LogoutPage(request):
    logout(request)
    return redirect('login')

def calculate_area(image_path):
    if not image_path:
        return 0
    image = cv2.imread(image_path)
    if image is None:
        return 0
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    _, thresh = cv2.threshold(gray, 127, 255, cv2.THRESH_BINARY)
    contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    total_area = sum(cv2.contourArea(contour) for contour in contours)
    return total_area

def calculate_seed_amount(area, seed_density):
    seed_amount = area * seed_density
    return seed_amount
