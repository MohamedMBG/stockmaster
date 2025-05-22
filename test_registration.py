"""
Test script for registration and login functionality.
This script will test both valid and invalid registration attempts,
as well as login functionality with the fixed code.
"""

import os
import sys
import django
from django.test import Client
from django.urls import reverse
from django.contrib.auth import get_user_model

# Set up Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'stockmaster.settings')
django.setup()

User = get_user_model()

def test_registration():
    """Test client registration functionality."""
    print("\n=== Testing Registration ===")
    
    client = Client()
    
    # Test 1: Valid registration
    print("\nTest 1: Valid registration")
    valid_data = {
        'username': 'testclient',
        'email': 'testclient@example.com',
        'first_name': 'Test',
        'last_name': 'Client',
        'phone_number': '1234567890',
        'user_address': '123 Test Street',
        'password1': 'TestPassword123!',
        'password2': 'TestPassword123!',
    }
    
    response = client.post(reverse('register'), valid_data, follow=True)
    print(f"Status code: {response.status_code}")
    print(f"Redirected to: {response.redirect_chain}")
    
    # Check if user was created
    user_exists = User.objects.filter(username='testclient').exists()
    print(f"User created: {user_exists}")
    
    if user_exists:
        user = User.objects.get(username='testclient')
        print(f"User details: {user.username}, {user.email}, {user.first_name}, {user.last_name}, {user.phone_number}")
    
    # Test 2: Missing required fields
    print("\nTest 2: Missing required fields")
    invalid_data = {
        'username': 'testclient2',
        'email': 'testclient2@example.com',
        # Missing first_name, last_name, phone_number
        'password1': 'TestPassword123!',
        'password2': 'TestPassword123!',
    }
    
    response = client.post(reverse('register'), invalid_data)
    print(f"Status code: {response.status_code}")
    print(f"Form errors present: {'form' in response.context and response.context['form'].errors}")
    
    if 'form' in response.context:
        print(f"Form errors: {response.context['form'].errors}")
    
    # Test 3: Password mismatch
    print("\nTest 3: Password mismatch")
    invalid_data = {
        'username': 'testclient3',
        'email': 'testclient3@example.com',
        'first_name': 'Test',
        'last_name': 'Client',
        'phone_number': '1234567890',
        'password1': 'TestPassword123!',
        'password2': 'DifferentPassword123!',
    }
    
    response = client.post(reverse('register'), invalid_data)
    print(f"Status code: {response.status_code}")
    print(f"Form errors present: {'form' in response.context and response.context['form'].errors}")
    
    if 'form' in response.context:
        print(f"Form errors: {response.context['form'].errors}")

def test_login():
    """Test login functionality."""
    print("\n=== Testing Login ===")
    
    client = Client()
    
    # Create a test user if not exists
    if not User.objects.filter(username='logintest').exists():
        User.objects.create_user(
            username='logintest',
            email='logintest@example.com',
            password='TestPassword123!',
            first_name='Login',
            last_name='Test',
            phone_number='9876543210',
            role='CLIENT'
        )
    
    # Test 1: Valid login
    print("\nTest 1: Valid login")
    valid_data = {
        'username': 'logintest@example.com',  # Using email as username
        'password': 'TestPassword123!',
    }
    
    response = client.post(reverse('login'), valid_data, follow=True)
    print(f"Status code: {response.status_code}")
    print(f"Redirected to: {response.redirect_chain}")
    print(f"User authenticated: {response.context['user'].is_authenticated}")
    
    # Test 2: Invalid credentials
    print("\nTest 2: Invalid credentials")
    invalid_data = {
        'username': 'logintest@example.com',
        'password': 'WrongPassword123!',
    }
    
    response = client.post(reverse('login'), invalid_data)
    print(f"Status code: {response.status_code}")
    print(f"Form errors present: {'form' in response.context and response.context['form'].errors}")
    
    if 'form' in response.context:
        print(f"Form errors: {response.context['form'].errors}")

if __name__ == '__main__':
    test_registration()
    test_login()
