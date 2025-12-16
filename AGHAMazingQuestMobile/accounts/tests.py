from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status

from .models import EmailOTP, User
from unittest.mock import patch
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken


class AccountsAuthTests(APITestCase):
	"""Tests for OTP auth flow and profile endpoint.

	These tests exercise the same code paths your Unity client will use:
	- POST /api/auth/otp/request/ to create an OTP
	- POST /api/auth/otp/verify/ to exchange OTP for JWT tokens
	- GET /api/auth/profile/ with the access token to retrieve the user
	"""

	def test_otp_request_and_verify_creates_user_and_returns_tokens(self):
		email = "ci-tester@example.com"

		# 1) Request OTP
		resp = self.client.post(
			reverse('otp_request'),
			data={"email": email},
			format='json'
		)
		self.assertEqual(resp.status_code, status.HTTP_200_OK)

		# There should be an OTP row for this email
		otp = EmailOTP.objects.filter(email=email).order_by('-created_at').first()
		self.assertIsNotNone(otp, "OTP object was not created")

		# 2) Verify OTP using the code stored in DB (simulates reading email in tests)
		resp = self.client.post(
			reverse('otp_verify'),
			data={"email": email, "code": otp.code},
			format='json'
		)
		self.assertEqual(resp.status_code, status.HTTP_200_OK)
		payload = resp.json()
		self.assertIn('access', payload)
		self.assertIn('refresh', payload)

		access = payload['access']

		# 3) Using access token, fetch profile
		self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {access}')
		resp = self.client.get(reverse('api_profile'))
		self.assertEqual(resp.status_code, status.HTTP_200_OK)
		body = resp.json()
		self.assertEqual(body.get('email'), email)

		# Ensure the user was created in the DB
		user = User.objects.filter(email=email).first()
		self.assertIsNotNone(user)


	def test_invalid_otp_fails(self):
		email = "ci-tester2@example.com"
		# request OTP
		resp = self.client.post(reverse('otp_request'), {"email": email}, format='json')
		self.assertEqual(resp.status_code, status.HTTP_200_OK)

		# attempt verify with wrong code
		resp = self.client.post(reverse('otp_verify'), {"email": email, "code": '000000'}, format='json')
		self.assertEqual(resp.status_code, status.HTTP_400_BAD_REQUEST)

	def test_username_password_login_refresh_and_logout(self):
		# create a user that will authenticate with username/password
		username = 'testuser'
		password = 's3cureP@ssw0rd'
		email = 'testuser@example.com'
		User.objects.create_user(username=username, email=email, password=password)

		# login with username/password
		resp = self.client.post('/api/auth/login/', {"username": username, "password": password}, format='json')
		self.assertEqual(resp.status_code, status.HTTP_200_OK)
		data = resp.json()
		# dj-rest-auth with REST_USE_JWT should return access/refresh tokens
		self.assertIn('access', data)
		self.assertIn('refresh', data)

		access = data['access']
		refresh = data['refresh']

		# fetch profile using access token
		self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {access}')
		resp = self.client.get(reverse('api_profile'))
		self.assertEqual(resp.status_code, status.HTTP_200_OK)
		self.assertEqual(resp.json().get('email'), email)

		# refresh access token
		resp = self.client.post('/api/auth/token/refresh/', {"refresh": refresh}, format='json')
		self.assertEqual(resp.status_code, status.HTTP_200_OK)
		self.assertIn('access', resp.json())

		# logout (blacklist the refresh token)
		# logout endpoint expects Authorization header and refresh in body
		self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {access}')
		resp = self.client.post('/api/auth/logout/', {"refresh": refresh}, format='json')
		# dj-rest-auth usually returns 200 or 204 on successful logout
		self.assertIn(resp.status_code, (status.HTTP_200_OK, status.HTTP_204_NO_CONTENT))

		# attempt to refresh again with same refresh token should fail after blacklist
		resp = self.client.post('/api/auth/token/refresh/', {"refresh": refresh}, format='json')
		self.assertNotEqual(resp.status_code, status.HTTP_200_OK)

	@patch('accounts.social.GoogleLogin.post')
	def test_google_social_login_returns_tokens(self, mock_post):
		"""Mock the Google social login view to simulate token-exchange flow.

		We patch `GoogleLogin.post` so tests don't depend on external Google APIs.
		The patched method returns JWT tokens for a test user.
		"""
		email = 'googleuser@example.com'
		username = 'googleuser'

		# Ensure user exists (social login would create if needed)
		user, _ = User.objects.get_or_create(email=email, defaults={'username': username})

		# Create JWT tokens for that user
		refresh = RefreshToken.for_user(user)
		tokens = {'access': str(refresh.access_token), 'refresh': str(refresh)}

		# Patch the view's post to return the tokens
		mock_post.return_value = Response(tokens, status=200)

		# Call the endpoint — the patched method will return our tokens
		resp = self.client.post('/api/auth/google/', {'access_token': 'fake-token'}, format='json')
		self.assertEqual(resp.status_code, status.HTTP_200_OK)
		body = resp.json()
		self.assertIn('access', body)
		self.assertIn('refresh', body)

