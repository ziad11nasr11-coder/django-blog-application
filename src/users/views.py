from django.shortcuts import render
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect
from .forms import LoginForm
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST

def login_view(request):
    if request.user.is_authenticated:
        return redirect("index")

    form = LoginForm()

    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data["username"]
            password = form.cleaned_data["password"]

            user = authenticate(request, username=username, password=password)

            if user is not None:
                login(request, user)
                return redirect("index")
            else:
                form.add_error(None, "Invalid username or password")

    return render(request, "userss/login.html", {"form": form})


@login_required
@require_POST
def logout_view(request):
    logout(request)
    return redirect("login")
