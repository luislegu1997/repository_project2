from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.utils import timezone


from .models import User, Listing, Watchlist, Bid, Comment

from django import forms


class listingForm(forms.ModelForm):
    class Meta:
        model = Listing
        fields = ('Title', 'Description', 'Price', 'imgURL','Category')

def index(request):

    return render(request, "auctions/index.html", {

        'listings': Listing.objects.all()
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
    
    if request.method == "POST":

        form = listingForm(request.POST)

        if form.is_valid():

            listing = form.save(commit=False)

            listing.user = request.user

            listing.time = timezone.now()
            
            listing.save()

            return HttpResponseRedirect(reverse('index'))
        
        return HttpResponseRedirect(reverse('create'))


    else:

        form = listingForm()

        return render(request, "auctions/create_listing.html", {
            'form' : form
        })



def item_page(request, item):

    selected_item = Listing.objects.get(id=item)

    your_item = False

    bids_so_far = 0

    bid_winning_so_far = False

    watchlist_items= True

    you_won = False

    comments_of_item = selected_item.item_comments.all()

    try:

        usr = User.objects.get(username=request.user)

        if usr == selected_item.user :

            your_item = True


        if selected_item.winner == usr:

            you_won = True

    
    except:

        print("user not found")


    try:

        Watchlist.objects.get(listing=selected_item, user=usr)

    except:

        watchlist_items= False


    try:

        current_bids = Bid.objects.filter(listing=selected_item)

        bids_so_far = len(current_bids)
       
        current_bids = sorted(current_bids, key=lambda bid: bid.Value, reverse=True)[0]

        if current_bids.user == request.user:

            bid_winning_so_far = True


    except:

        current_bids = Bid( Value= selected_item.Price, user= usr, listing=selected_item)

        current_bids.save()


    return render(request, "auctions/item_page.html", {

        'item': selected_item,

        'watchlist_items' : watchlist_items,

        'current_bid' : current_bids,

        'your_item': your_item,

        'bids_so_far': bids_so_far,

        'bid_winning_so_far': bid_winning_so_far,

        'you_won': you_won,

        'comments_of_item': comments_of_item

    })



def WatchlistAdd(request, item):

    selected_item = Listing.objects.get(id=item)

    user = User.objects.get(username=request.user)

    data = Watchlist(listing=selected_item, user=user)

    data.save()

    return HttpResponseRedirect(reverse('index'))


def RemoveWatchlist(request, item):

    selected_item = Listing.objects.get(id=item)

    user = User.objects.get(username=request.user)

    data= Watchlist.objects.get(listing=selected_item, user=user)

    data.delete()

    return HttpResponseRedirect(reverse('index'))




def Bid_money(request, item):

    selected_item = Listing.objects.get(id=item)

    user = User.objects.get(username=request.user)

    bd = request.POST['bid_made']

    all_bids = selected_item.listing_bids.all()

    all_bids = sorted(all_bids, key=lambda bid: bid.Value, reverse=True)

    if selected_item.user == user:

        return render(request, 'auctions/error.html', {

           'message': "you can´t bid your own listing"
       })

    elif float(bd) < float(all_bids[0].Value):

       return render(request, 'auctions/error.html', {

           'message': "bid must be higher"
       })

    data = Bid(Value=bd, user=user, listing=selected_item)

    data.save()

    return HttpResponseRedirect(reverse('index'))


def Delete_item(request, item):

    selected_item = Listing.objects.get(id=item)

    selected_item.delete()

    return HttpResponseRedirect(reverse('index'))



def Close(request, item):

    selected_item = Listing.objects.get(id=item)

    bids = selected_item.listing_bids.all()

    winner_bid = sorted(bids, key=lambda bid: bid.Value, reverse=True)[0]

    winner = User.objects.get(username=winner_bid.user )

    selected_item.winner = winner

    selected_item.save()

    return HttpResponseRedirect(reverse('item_page', kwargs={'item': selected_item.id}))



def Comment_add(request, item):

    selected_item = Listing.objects.get(id=item)

    comment_posted = request.POST['comment'] 

    usr = User.objects.get(username=request.user)

    data = Comment(entry=comment_posted, user= usr, listing=selected_item)
    
    data.save()

    return HttpResponseRedirect(reverse('item_page', kwargs={"item": selected_item.id}))



def Watchlist_display(request):

   usr = User.objects.get(username=request.user)

   watchlst = usr.This_User_Watchlist.all()

   return render(request, "auctions/watchlist.html", {

       'watchlst' : watchlst
   })

def Categories(request):

    return render(request, "auctions/categories.html", {

        'categories' : ['Home','Fashion','Jewlelery','Electronics','Toys','Other']
    })


def Category_selected(request, category):

    return render(request, 'auctions/index.html', {

        'listings' : Listing.objects.filter(Category=category)
    })