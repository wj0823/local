from django.contrib import messages
from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
# Create your views here.
from Core.models import Info
# from django.contrib.auth.models import User
from .models import User, Score


def index(request):
    return render(request,'index.html')


def signup(request):
    if request.method == "POST":
        email = request.POST.get("email", "")
        if User.objects.filter(email=email).exists():
        #     messages.warning(request,"Email Already Exist!")
            return render(request, 'signup.html')
        username = request.POST.get("username", "")
        if User.objects.filter(username=username).exists():
            #     messages.warning(request,"Email Already Exist!")
            return render(request, 'signup.html')

        password = request.POST.get("pass", "")
        password1 = request.POST.get("pass2", "")
        role = request.POST.get("role", "")
        if password1 != password:
            return HttpResponse("Password and Confirm Password did not match")
        user_obj = User.objects.create_user(username=username, email=email)
        user_obj.set_password(password)
        user_obj.save()
        Info.objects.create(user=user_obj, role=role)
        return redirect('login')

    return render(request, 'signup.html')


def check_mail(request):
    data1 = ''
    data2 = ''

    if User.objects.filter(email=request.GET["email"]).exists():
        data1 = "Email Already Exist!"
    if User.objects.filter(username=request.GET["username"]).exists():
            data2 = "username already in use!"
    data = {
        "data1":data1,
        "data2":data2,
    }
    return JsonResponse(data, safe=False)


def authorize(request):
    if request.user:
        if Info.objects.filter(user__username=request.user.username).exists():
            info = Info.objects.get(user__username=request.user.username)
            if info.role == 'S':
                return render(request, 'index_unity.html')
            else:
                scores = Score.objects.all().order_by('-id')
                return render(request, 'teacher.html', {
                    'scores': scores
                })
    messages.error(request, "User does not exist!")
    return redirect('login')


def updateValue(request):
    if request.method == "POST" and request.user.is_authenticated:
        user_id = request.user.pk
        user = User.objects.filter(pk=user_id).first()
        score = request.POST.get("currentScore", "0")
        max_score = request.POST.get("highScore", "0")
        score = Score.objects.create(user=user, score=score, max_score=max_score)
        print(currentScore + " : " + highScore);
        return HttpResponse("Success!!!" + currentScore + ":" + highScore)
        
# def authorize(request):
#     if request.method=='POST':
#         user_name = request.POST.get("username","")
#         password = request.POST.get("pass","")
#         if User.objects.filter(username=user_name).exists():
#             user_obj = User.objects.get(username=user_name)
#             print(user_obj.check_password(password))
#             if user_obj.check_password(password)==True:
#                 print("in obj")
#                 if Info.objects.filter(user__username=user_name).exists():
#                     info = Info.objects.get(user__username=user_name)
#                     request.session["username"] = info.user.username
#                     if info.role=='S':
#                         return render(request,'index_unity.html')
#                     else:
#                         return render(request,'teacher.html')
#             return HttpResponse("Invalid Password")
#         messages.error(request, "User does not exist!")
#         return render(request, 'index.html')
