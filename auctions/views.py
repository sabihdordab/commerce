from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from . import util
from .models import *
import datetime


def index(request):
    listings = Listing.objects.exclude(isclosed = True).all().order_by('id').reverse()
    return render(request, "auctions/index.html" , {
        'listings' : listings,
    })


def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "auctions/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "auctions/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "auctions/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "auctions/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "auctions/register.html")

def create_listing(request):

    user = request.user
    if user.id is None :
        return render(request, "auctions/login.html", {
            "message": "Please login first"
        })

    if request.method == "POST":
        listing = Listing(owner = user,title = request.POST['title'] , description = request.POST['description'] ,
        starting_bid = request.POST['bid'] , category = request.POST['category'] , date = datetime.datetime.now() , winner=user )
        bid = Bid(user=user,bid=request.POST['bid'],date=datetime.datetime.now())
        bid.save()
        if request.POST['image url']:
            listing.image_url = request.POST['image url']
        else :
            listing.image_url = "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcRFG5-XTBYvoFjptCqHdiL_PXjkphJ3yGDxJ_tska9MH2XJWNQ5EIOO0maRAVRCqfXT4oI&usqp=CAU"
        listing.save()
        listing.bids.add(bid)
        return HttpResponseRedirect(reverse("index"))
    # request method = GET :
    return render(request, 'auctions/create_listing.html' ,{
        'categories' : util.category_list })
    

def listing_page(request,id):

    user = request.user
    if user.id is None :
        return render(request, "auctions/login.html", {
            "message": "Please login first"
        })

    try:
        listing = Listing.objects.get(id=id)
        current_bid , min_bid = util.calculate_the_current_bid(listing)
        is_owner = False
        is_added = False

        try:
            if Watch_list.objects.get(user=user,listing=listing):
                is_added = True
        except:
            pass

        if listing.owner == user:
            is_owner = True
        
        if listing.isclosed :
            listing.winner = util.who_is_winner(listing)
        
        return render(request, 'auctions/listing_page.html',{
            'listing' : listing,
            'comments' : listing.comments.all().order_by('id').reverse(),
            'is_added' : is_added ,
            'is_owner' : is_owner,
            'current_bid': current_bid, 
            'min_bid' : min_bid ,
            'logged_user' : user
        })
    except:
        #listing not found 
        return render(request, 'auctions/page_not_found.html')


def add_comment(request,id):
    if request.method == "POST":
        listing = Listing.objects.get(id=id)
        new_comment = Comment(user = request.user , comment=request.POST['comment'] , date=datetime.datetime.now())
        new_comment.save()
        listing.comments.add(new_comment)
        listing.save()
        return HttpResponseRedirect(reverse('listing_page',args=(id,)))
    else:
        return HttpResponseRedirect(reverse('index'))
            
def add_bid(request,id):
    if request.method == "POST":
        listing = Listing.objects.get(id=id)
        user_bid = request.POST['user_bid']
        new_bid = Bid(user=request.user,bid=user_bid,date=datetime.datetime.now())
        new_bid.save()
        listing.bids.add(new_bid)
        return HttpResponseRedirect(reverse('listing_page',args=(id,)))
    # GET
    return HttpResponseRedirect(reverse('index'))

def watch_list(request):
    user = request.user
    if user.id is None :
        return render(request, "auctions/login.html", {
            "message": "Please login first"
        })

    return render(request, 'auctions/watchlist.html',{
            'watchLists' : Watch_list.objects.filter(user=user).all().order_by('id').reverse()
        })
    
def add_watch_list(request,id):
    user = request.user
    if user.id is None :
        return render(request, "auctions/login.html", {
            "message": "Please login first"
        })

    try:
        listing = Listing.objects.get(id=id)
        watch_list = Watch_list(user=user,listing=listing)
        watch_list.save()
        return HttpResponseRedirect(reverse('listing_page',args=(id,)))
    except:
        #listing not found 
        return render(request, 'auctions/page_not_found.html')

def remove_watch_list(request,id):
    user = request.user
    if user.id is None :
        return render(request, "auctions/login.html", {
            "message": "Please login first"
        })

    try :
        listing = Listing.objects.get(id=id)
    except:
        #listing not found 
        return render(request, 'auctions/page_not_found.html')

    try:
        watch_list = Watch_list.objects.get(user=user,listing=listing)
        watch_list.delete()
        return HttpResponseRedirect(reverse('listing_page',args=(id,)))
    except:
        return HttpResponseRedirect(reverse('listing_page',args=(id,)))

def categories(request):
    return render(request, 'auctions/categories.html', {
        'categories' : util.category_list
    })

def category(request,category_name):
    if category_name.title() not in util.category_list:
        return render(request, 'auctions/page_not_found.html')

    listings = Listing.objects.filter(category=category_name.title()).order_by('id').reverse().exclude(isclosed=True).all()
    return render(request, 'auctions/category.html',{
        'listings' : listings , 
        'category' : category_name.title()
    })

def close_listing(request,id):
    user = request.user
    if user.id is None :
        return render(request, "auctions/login.html", {
            "message": "Please login first"
        })
    
    try:
        listing = Listing.objects.get(id=id)
    except:
        #listing not found 
        return render(request, 'auctions/page_not_found.html')

    if user == listing.owner:  
        listing.isclosed = True
        listing.save()
        return HttpResponseRedirect(reverse('listing_page',args=(id,)))

    return HttpResponseRedirect(reverse('index'))
