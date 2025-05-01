from django.test import TestCase
from django.utils import timezone
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient
from rest_framework import status
from .models import Auction, Bid

User = get_user_model()

class AuctionModelTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
        self.auction = Auction.objects.create(
            title='Test Auction',
            description='Test Description',
            starting_price=100.00,
            start_time=timezone.now(),
            end_time=timezone.now() + timezone.timedelta(days=7),
            creator=self.user
        )

    def test_auction_creation(self):
        self.assertEqual(self.auction.title, 'Test Auction')
        self.assertEqual(self.auction.current_price, 100.00)
        self.assertTrue(self.auction.is_active)
        self.assertEqual(str(self.auction), 'Test Auction')

    def test_auction_status_update(self):
        self.auction.end_time = timezone.now() - timezone.timedelta(days=1)
        self.auction.update_status()
        self.assertFalse(self.auction.is_active)

class BidModelTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
        self.auction = Auction.objects.create(
            title='Test Auction',
            description='Test Description',
            starting_price=100.00,
            start_time=timezone.now(),
            end_time=timezone.now() + timezone.timedelta(days=7),
            creator=self.user
        )

    def test_bid_creation(self):
        bid = Bid.objects.create(
            auction=self.auction,
            bidder=self.user,
            amount=150.00
        )
        self.assertEqual(bid.amount, 150.00)
        self.assertEqual(self.auction.current_price, 150.00)
        self.assertEqual(str(bid), 'testuser - 150.00')

    def test_invalid_bid_amount(self):
        with self.assertRaises(ValueError):
            Bid.objects.create(
                auction=self.auction,
                bidder=self.user,
                amount=50.00
            )

class AuctionAPITests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
        self.client.force_authenticate(user=self.user)
        self.auction = Auction.objects.create(
            title='Test Auction',
            description='Test Description',
            starting_price=100.00,
            start_time=timezone.now(),
            end_time=timezone.now() + timezone.timedelta(days=7),
            creator=self.user
        )

    def test_create_auction(self):
        payload = {
            'title': 'New Auction',
            'description': 'New Description',
            'starting_price': 200.00,
            'start_time': timezone.now(),
            'end_time': timezone.now() + timezone.timedelta(days=5)
        }
        response = self.client.post('/api/auctions/create/', payload)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Auction.objects.count(), 2)

    def test_place_bid(self):
        payload = {'amount': 150.00}
        response = self.client.post(
            f'/api/auctions/{self.auction.id}/bids/create/',
            payload
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(self.auction.bids.count(), 1)
        self.assertEqual(self.auction.current_price, 150.00)

    def test_end_auction(self):
        response = self.client.put(f'/api/auctions/{self.auction.id}/end/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.auction.refresh_from_db()
        self.assertFalse(self.auction.is_active)
