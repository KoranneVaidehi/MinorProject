from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib import messages

from .models import MediaUpload
from .utils import detect_face, detect_faces_video


#  Home
def home(request):
    return render(request, "home.html")


#  Login
def login_view(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(request, username=username, password=password)

        if user:
            login(request, user)
            return redirect("dashboard")
        else:
            messages.error(request, "Invalid username or password")

    return render(request, "login.html")


#  Register
def register_view(request):
    if request.method == "POST":
        username = request.POST.get("username")
        email = request.POST.get("email")
        password = request.POST.get("password")
        confirm_password = request.POST.get("confirm_password")

        if password != confirm_password:
            messages.error(request, "Passwords do not match")
            return redirect("register")

        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already exists")
            return redirect("register")

        User.objects.create_user(
            username=username,
            email=email,
            password=password
        )

        messages.success(request, "Account created successfully")
        return redirect("login")

    return render(request, "register.html")


#  Dashboard
def dashboard(request):
    if not request.user.is_authenticated:
        return redirect("login")

    return render(request, "dashboard.html")


#  Logout
def logout_view(request):
    logout(request)
    return redirect("login")


#  Upload + Face Detection
def upload_media(request):
    if request.method == "POST":
        file = request.FILES.get("file")

        if not file:
            return render(request, "upload.html", {"msg": "No file selected"})

        media = MediaUpload.objects.create(
            user=request.user,
            file=file
        )

        file_path = media.file.path

        #  Decide image or video
        if file.content_type.startswith("image"):
            faces, heatmap_path = detect_face(file_path)
        else:
            faces, heatmap_path = detect_faces_video(file_path)

        return render(
            request,
            "result.html",
            {
                "media": media,
                "faces": faces,
                "heatmap": heatmap_path
            }
        )

    return render(request, "upload.html")