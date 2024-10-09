from django.forms.utils import ErrorList

class HiddenErrorList(ErrorList):
    def __str__(self):
        return self.as_hidden()

    def as_hidden(self):
        return ''
    
def update_price(auctions):
    for auction in auctions:
        max_bid = auction.bids.order_by('-price').first()
        if max_bid is None:
            max_bid = auction.start_bid
        else:
            max_bid = max_bid.price
        auction.price = max_bid # ik it's not the best but I don't have time for this xd