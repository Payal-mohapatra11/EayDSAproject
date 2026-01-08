from allauth.account.signals import user_signed_up, user_logged_in
from django.dispatch import receiver

# When Google account is used for the FIRST time
@receiver(user_signed_up)
def after_google_signup(request, user, **kwargs):
    print("NEW USER SIGNED UP:", user.email)
    # You can do custom actions here
    # Example:
    # user.username = user.email.split("@")[0]
    # user.save()

# When Google user logs in again
@receiver(user_logged_in)
def after_google_login(request, user, **kwargs):
    print("RETURNING USER LOGGED IN:", user.email)
