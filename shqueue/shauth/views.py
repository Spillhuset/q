from django.shortcuts import redirect
from jwt import decode
from django.conf import settings
from django.contrib.auth.models import User
from django.contrib.auth import login

def auth(request):
    token = request.POST.get("shauth")
    decoded = None

    if token:
        # verify token
        try:
          decoded = decode(token, settings.SHAUTH_KEY, algorithms=["HS256"])
          if decoded:
              users = User.objects.filter(username=decoded["id"])
              if users: user = users[0]
              else: user = User.objects.create_user(decoded["id"])
              user.first_name = decoded["name"]

              flags = decoded["userFlags"]
              # Systems
              if flags & 1 << 11:
                user.is_superuser = True
                user.is_staff = True

              user.save()
              login(request, user)
              return redirect("/")
        except Exception as e:
          print("token:", token)
          print("decoded:", decoded)
          print("exception:", e)
          pass

    return redirect("https://shauth.but-it-actually.works/?state=shqueue");
