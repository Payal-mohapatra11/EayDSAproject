from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .forms import CustomSignupForm
from django.contrib.auth.models import User
from django.db.models import Q  #Q()-Query wrapper /Without Q, Django cannot combine conditions like that.
from allauth.socialaccount.models import SocialLogin
from allauth.socialaccount.models import SocialAccount
from .models import Profile
# Create your views here.
def SignupView(request):
    #Auto-fill username and email if coming from google
    google_email = request.session.get("google_email")
    if request.method == "GET" and google_email:
         suggested_username = google_email.split("@")[0]
         base = suggested_username
         counter=1
         while User.objects.filter(username=suggested_username).exists():
             suggested_username = f"{base}{counter}"
             counter=counter+1
        #Prefill form with Google data
         form = CustomSignupForm(initial={"email":google_email,"username":suggested_username})
         return render(request,"authapp/signup.html",{"form":form})
         
         #Handle form submission   
    if request.method == "POST":
        form = CustomSignupForm(request.POST)
        if form.is_valid():
            user = form.save()
            Profile.objects.create(user=user,full_name=user.username,phone=form.cleaned_data["phone"])
            print("User created:", user.username)
            
            google_email = request.session.get("google_email")
            google_uid = request.session.get("google_uid")
            print("session email =",google_email)
            print("session uid=",google_uid)
            #save google account
            if google_email and google_uid:
                SocialAccount.objects.create(user=user,provider="google",uid=google_uid)
                del request.session["google_email"]
                del request.session["google_uid"]
                print("Linked Google account to user:")
            return redirect('/auth/login/')
        else:
            print("Form errors:",form.errors)
    #If not Get or post request 
    form = CustomSignupForm()
    return render(request,"authapp/signup.html",{"form":form}) 

def LoginView(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        #CHECK IF THE USERNAME IS EXISTS 
        user_qs = User.objects.filter(Q(username=username) | Q(email=username))
        if not user_qs.exists():
            return render(request,"authapp/login.html",{"error":"Invalid username or email"})
        
        user_obj = user_qs.first()
        
        #Block login if user is inactive
        if not user_obj.has_usable_password():
            return render(request,"authapp/login.html",{"error":"This account is registered via Google. Please use Google Sign-In."})
        user = authenticate(request,username=user_obj.username,password=password)
        if user:
            login(request,user)
            return redirect( "success")
        return render(request, "authapp/login.html", {
            "error": "Invalid credentials"
})
           
        # else:
        #     return render(request,"authapp/login.html",{"error":"Invalid credentials"})
    return render(request,"authapp/login.html")

@login_required
def success_view(request):
    return render(request, "authapp/success.html")

def logout_view(request):
    logout(request)
    return redirect("login")
