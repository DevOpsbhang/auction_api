from django.urls import path
from .views import (
    AuctionListView,
    AuctionCreateView,
    AuctionDetailView,
    BidCreateView
)

urlpatterns = [
    path('', AuctionListView.as_view(), name='auction-list'),
    path('create/', AuctionCreateView.as_view(), name='auction-create'),
    path('<int:pk>/', AuctionDetailView.as_view(), name='auction-detail'),
    path('<int:pk>/bids/', BidCreateView.as_view(), name='bid-create'),
]
