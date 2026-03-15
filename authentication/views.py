from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib import messages
from django.shortcuts import render

def home(request):

    return render(request, "home.html")


def login_view(request):

    if request.method == "POST":

        username = request.POST["username"]
        password = request.POST["password"]

        user = authenticate(request, username=username, password=password)

        if user:
            login(request, user)
            return redirect("dashboard")

        else:
            messages.error(request, "Invalid username or password")

    return render(request,"login.html")


def register_view(request):

    if request.method == "POST":

        username = request.POST["username"]
        email = request.POST["email"]
        password = request.POST["password"]
        confirm_password = request.POST["confirm_password"]

        if password != confirm_password:
            messages.error(request,"Passwords do not match")
            return redirect("register")

        if User.objects.filter(username=username).exists():
            messages.error(request,"Username already exists")
            return redirect("register")

        User.objects.create_user(
            username=username,
            email=email,
            password=password
        )

        messages.success(request,"Account created successfully")

        return redirect("login")

    return render(request,"register.html")


def dashboard(request):

    if not request.user.is_authenticated:
        return redirect("login")

    return render(request,"dashboard.html")


def logout_view(request):

    logout(request)

    return redirect("login")


from django.shortcuts import render
from .models import MediaUpload

def upload_media(request):

    if request.method == "POST":

        file = request.FILES["file"]

        MediaUpload.objects.create(
            user=request.user,
            file=file
        )

        return render(request,"upload.html",{"msg":"Upload Successful"})

    return render(request,"upload.html")



from .models import MediaUpload
from .utils import detect_face


def upload_media(request):

    if request.method == "POST":

        file = request.FILES["file"]

        media = MediaUpload.objects.create(
            user=request.user,
            file=file
        )

        file_path = media.file.path

        face_count = detect_face(file_path)

        return render(
            request,
            "result.html",
            {
                "media": media,
                "faces": face_count
            }
        )

    return render(request,"upload.html")


from .utils import detect_face, detect_faces_video


def upload_media(request):

    if request.method == "POST":

        file = request.FILES["file"]

        media = MediaUpload.objects.create(
            user=request.user,
            file=file
        )

        file_path = media.file.path

        if file.content_type.startswith("image"):

            faces = detect_face(file_path)

        else:

            faces = detect_faces_video(file_path)

        return render(
            request,
            "result.html",
            {
                "media": media,
                "faces": faces
            }
        )

    return render(request,"upload.html")