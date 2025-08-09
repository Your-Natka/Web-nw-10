# pylint: disable=no-member

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth.decorators import login_required
from django.db.models import Count
from django.core.paginator import Paginator

from .models import Tag, Quote, Author
from .forms import QuoteForm


def main_view(request):
    quotes = Quote.objects.all().order_by('id')
    paginator = Paginator(quotes, 5)  # 5 цитат на сторінку

    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    return render(request, "quotes/index.html", {"page_obj": page_obj})


def signup(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect("home")
    else:
        form = UserCreationForm()
    return render(request, "registration/signup.html", {"form": form})


def author_detail(request, author_id):
    author = get_object_or_404(Author, id=author_id)
    return render(request, 'quotes/author_detail.html', {'author': author})


def top_tags(request):
    tags = Tag.objects.annotate(num_quotes=Count('quote')).order_by('-num_quotes')[:10]
    return render(request, 'quotes/top_tags.html', {'tags': tags})


def quotes_by_tag(request, tag_name):
    quotes = Quote.objects.filter(tags__name=tag_name)
    return render(request, 'quotes/quotes_by_tag.html', {
        'quotes': quotes,
        'tag': tag_name
    })

def latest_quotes(request):
    quotes = Quote.objects.order_by('-id')[:5]  # або '-created_at', якщо є поле дати
    return render(request, 'latest_quotes.html', {'quotes': quotes})

@login_required
def add_quote(request):
    if request.method == 'POST':
        form = QuoteForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('home')
    else:
        form = QuoteForm()
    return render(request, 'quotes/add_quote.html', {'form': form})


def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('home')
    else:
        form = AuthenticationForm()
    return render(request, 'quotes/login.html', {'form': form})

def logout_view(request):
    logout(request)
    return render(request, 'registration/logged_out.html')
