from .models import *
category_list = ["Fashion","Toys","Electronics","Home Accessories","Tools","Books","Beauty","Health","Etc"]

def calculate_the_current_bid(listing):
    if len(Listing.objects.get(id=listing.id).bids.all()) > 1 :
        current_bid = listing.bids.all().last().bid
        min_bid = listing.bids.all().last().bid + 1
    else:
        current_bid = listing.starting_bid
        min_bid = listing.starting_bid

    return (current_bid,min_bid)

def who_is_winner(listing):
    # default winner is listing.owner
    if len(listing.bids.all()):
        winner = listing.bids.all().last().user
    
    return winner