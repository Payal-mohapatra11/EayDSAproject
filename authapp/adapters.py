from allauth.account.adapter import DefaultAccountAdapter
from allauth.socialaccount.adapter import DefaultSocialAccountAdapter
from django.shortcuts import redirect
from django.contrib import messages
from django.contrib.auth.models import User


class CustomAccountAdapter(DefaultAccountAdapter):
    pass
class NoPromptAccountAdapter(DefaultSocialAccountAdapter):
    

    # Block Google users if email not registered
    def pre_social_login(self, request, sociallogin):
        email = sociallogin.account.extra_data.get("email")
        uid = sociallogin.account.uid

        print("🚀 pre_social_login TRIGGERED")
        print("📧 GOOGLE EMAIL =", email)
        print("🆔 GOOGLE UID =", uid)

        if not email:
            return redirect('/auth/signup/')

        # If user exists -> normal flow
        if User.objects.filter(email=email).exists():
            return

        # NEW USERS -> Save in session
        request.session["google_email"] = email
        request.session["google_uid"] = uid
        request.session.modified = True  # <-- IMPORTANT

        print("💾 STORED IN SESSION FOR SIGNUP")

        return redirect('/auth/signup/')
    # Avoid error page
    def authentication_error(self, request, provider_id, error=None, exception=None, extra_context=None):
        messages.error(request, "Google login failed. Try again.")
        return redirect('/auth/login/')

    #     # REQUIRED: proper signature to avoid TypeError
    # def new_user(self, request, sociallogin):
    #     user = super().new_user(request, sociallogin)
    #     return user