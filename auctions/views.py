from rest_framework import generics, permissions, status
from rest_framework.response import Response
from django.utils import timezone
from .models import Auction, Bid
from .serializers import (
    AuctionSerializer,
    CreateAuctionSerializer,
    PlaceBidSerializer,
    BidSerializer
)
from django.shortcuts import get_object_or_404

class AuctionListCreateView(generics.ListCreateAPIView):
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    
    def get_serializer_class(self):
        if self.request.method == 'POST':
            return CreateAuctionSerializer
        return AuctionSerializer

    def get_queryset(self):
        queryset = Auction.objects.all()
        if self.request.query_params.get('active'):
            queryset = queryset.filter(is_active=True)
        return queryset

    def perform_create(self, serializer):
        serializer.save(creator=self.request.user)

class AuctionDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Auction.objects.all()
    serializer_class = AuctionSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def perform_update(self, serializer):
        if serializer.instance.creator != self.request.user:
            raise permissions.PermissionDenied("You can only update your own auctions")
        serializer.save()

    def perform_destroy(self, instance):
        if instance.creator != self.request.user:
            raise permissions.PermissionDenied("You can only delete your own auctions")
        instance.delete()

class BidCreateView(generics.CreateAPIView):
    serializer_class = PlaceBidSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_auction(self):
        return get_object_or_404(Auction, pk=self.kwargs['pk'])

    def create(self, request, *args, **kwargs):
        auction = self.get_auction()
        if not auction.is_active:
            return Response(
                {"detail": "This auction is closed."},
                status=status.HTTP_400_BAD_REQUEST
            )

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        try:
            bid = serializer.save(
                auction=auction,
                bidder=request.user
            )
        except ValueError as e:
            return Response(
                {"detail": str(e)},
                status=status.HTTP_400_BAD_REQUEST
            )

        return Response(
            BidSerializer(bid, context=self.get_serializer_context()).data,
            status=status.HTTP_201_CREATED
        )
