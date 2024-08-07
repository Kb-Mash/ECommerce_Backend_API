from django.test import TestCase
from django.contrib.auth import get_user_model
from .models import Customer
from django.core.exceptions import ValidationError

User = get_user_model()


class CustomerModelTests(TestCase):
    def setUp(self):
        # Create user instance for customer
        self.user = User.objects.create_user(
                username='testuser',
                password='password123',
                first_name='John',
                last_name='Doe',
                email='john@example.com'
        )

        # Create customer instance linked to user
        self.customer = Customer.objects.create(
                user=self.user,
                phone_number='123-456-7890',
                payment_token='abc123'
        )

    def test_customer_creation(self):
        # Test if customer is created correctly
        self.assertEqual(self.customer.user, self.user)
        self.assertEqual(self.customer.phone_number, '123-456-7890')
        self.assertEqual(self.customer.payment_token, 'abc123')
        self.assertIsNotNone(self.customer.created_at)

    def test_string_representation(self):
        # Test string representation of customer
        expected_string = f'{self.user.first_name} {self.user.last_name} ({self.user.email})'
        self.assertEqual(str(self.customer), expected_string)

    def test_customer_phone_number_blank(self):
        # Test that number can't be blank
        user2 = User.objects.create_user(
            username='testuser2',
            password='passw456',
            first_name='Sam',
            last_name='Smith',
            email='sam@example.com'
        )

        with self.assertRaises(ValidationError):
            customer = Customer.objects.create(
                user=user2,
                phone_number='',
                payment_token='abc123'
            )
            customer.full_clean()  # Manually trigger validation

    def test_customer_payment_token_null(self):
        # Test that payment_token can be null
        user3 = User.objects.create_user(
            username='testuser3',
            password='password456',
            first_name='Nerd',
            last_name='Smith',
            email='nerd@example.com'
        )

        customer = Customer.objects.create(
            user=user3,
            phone_number='987-654-3210',
            payment_token=None
        )

        self.assertIsNone(customer.payment_token)
