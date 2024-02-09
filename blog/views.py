import datetime
from django.views import View

from django.contrib.auth import logout, authenticate, login
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.views.generic import TemplateView, ListView

from blog.forms import LoginForm, UserRegistrationForm, PostCreateForm
from blog.models import Post, User
from django.contrib.auth.mixins import LoginRequiredMixin


class HomePageView(ListView):
    model = Post
    template_name = 'blog/home.html'


class AboutView(TemplateView):
    template_name = 'blog/about.html'


class NewPostView(TemplateView):
    template_name = "blog/post_form.html"


class UserPostView(TemplateView):
    template_name = "blog/user_posts.html"


class PostDetailView(TemplateView):
    template_name = "blog/post_detail.html"


def home_page(request):
    if request.user.is_authenticated:
        posts = Post.objects.exclude(author=request.user).filter(is_active=True).order_by("published")
    else:
        posts = Post.objects.all().filter(is_active=True).order_by("published")

    return render(request, "blog/home.html", context={"posts": posts})


def post_detail(request, pk):
    post = Post.objects.get(pk=pk)
    return render(request, "blog/post_detail.html", {"post": post})


# @login_required()
# def post_create(request):
#     if request.method == "POST":
#         form = PostCreateForm(request.POST)
#         if form.is_valid():
#             post = Post(title=form.cleaned_data["title"], content=form.cleaned_data["content"], is_active=form.cleaned_data["is_active"])
#             post.author = request.user
#             post.published = datetime.datetime.now().strftime("%Y-%m-%d")
#             post.save()
#             messages.success(request, "post successfully created")
#             return redirect(reverse('blog:user-profile', kwargs={"username":request.user.username}))
#         else:
#             return render(request, "blog/post_form.html", {"form": form})
#     else:
#         form = PostCreateForm()
#         return render(request, "blog/post_form.html", {"form": form})
    


class post_create(View, LoginRequiredMixin):
    def post(self, request):
        form = PostCreateForm
        if form.is_valid():
            post = Post(title = form.cleaned_data("title"), content = form.cleaned_data["content"], is_active= form.cleaned_data["is_active"])
            post.author = request.user
            post.published = datetime.datetime.now().strftime("%Y-%m-%d")
            post.save()
            messages.success(request, "post successfully created")
            return redirect(reverse('blog:user-profile', kwargs = {"username": request.user.username}))
        else:
            return render(request, "blog/post_form.html", {"form": form})





@login_required
def user_profile(request, username):
    posts = Post.objects.filter(author__username=username)
    user = get_object_or_404(User, username=username)
    first_name = user.first_name
    last_name = user.last_name
    return render(request, "blog/user_posts.html", {"posts": posts,
                                                    "first_name": first_name,
                                                    "last_name": last_name})


@login_required
def logout_view(request):
    messages.info(request, f"{request.user.username} user successfulley loged out")
    logout(request)
    return redirect("blog:home-page")


# def login_view(request):
#     if request.method == "POST":
#         form = LoginForm(request.POST)
#         if form.is_valid():
#             user = authenticate(request, username=request.POST.get("username"), password=request.POST.get("password"))
#             if user is not None:
#                 login(request, user)
#                 messages.success(request, "user succesfully loged in")
#                 return redirect("blog:home-page")
#             else:
#                 messages.warning(request, "User not found")
#                 return redirect("blog:login-page")
#         else:
#             return render(request, "blog/login.html", {"form": form})

#     else:
#         form = LoginForm()
#     return render(request, "blog/login.html", {"form": form})


class login_view(View):
    def get(self, request):
        form = LoginForm()
        return render(request, "blog/login.html", {"form":form})
    
    def post(self, request):
        form = LoginForm(data=request.POST)
        if form.is_valid():
            username = form.cleaned_data["username"]
            password = form.cleaned_data["password"]
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                print(request.COOKIES)
                messages.success(request, "user successfully logged in")
                return redirect("blog:home-page")
            else:
                messages.error(request, "Username or password wrong")
                return redirect("blog:login")

        else:
            return render(request, "blog/login.html", {"form": form})

# def register_view(request):
#     form = UserRegistrationForm()
#     if request.method == "POST":
#         form = UserRegistrationForm(request.POST, request.FILES)
#         if form.is_valid():
#             form.save()
#             messages.success(request, "User successfully registered")
#             return redirect('blog:login-page')
#         else:
#             return render(request, "blog/register.html", {"form": form})
#     else:
#         return render(request, "blog/register.html", {"form": form})
    

class register_view(View):
    def get(self, request):
        form = UserRegistrationForm()
        return render(request, "blog/register.html", {"form": form})
    
    def post(self, request):
        form = UserRegistrationForm(data=request.POST)
        if form.is_valid():
            messages.success(request, "User successfully registered")
            form.save()
            return redirect("blog:login-page")
        else:
            return render(request, "blog/register.html", {"form": form})   

