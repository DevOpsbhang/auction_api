from django.urls import path
from .views import (
    AuctionListCreateView,
    AuctionDetailView,
    BidCreateView
)

urlpatterns = [
    path('', AuctionListCreateView.as_view(), name='auction-list'),
    path('<int:pk>/', AuctionDetailView.as_view(), name='auction-detail'),
    path('<int:pk>/bids/', BidCreateView.as_view(), name='bid-create'),
]
