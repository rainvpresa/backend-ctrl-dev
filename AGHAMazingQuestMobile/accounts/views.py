from django.utils import timezone
from django.conf import settings
from django.core.mail import send_mail

from rest_framework import permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.generics import RetrieveAPIView
from rest_framework.permissions import IsAuthenticated

from .models import EmailOTP, User
from .serializers import UserSerializer, OTPRequestSerializer, OTPVerifySerializer

import random
from datetime import timedelta
from django.contrib.auth.forms import PasswordResetForm, SetPasswordForm
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_decode
from django.utils.encoding import force_str


class ProfileView(RetrieveAPIView):
	permission_classes = [IsAuthenticated]
	serializer_class = UserSerializer

	def get_object(self):
		return self.request.user


class OTPRequestView(APIView):
	"""Request an OTP to be sent to the provided email."""

	permission_classes = [permissions.AllowAny]

	def post(self, request):
		serializer = OTPRequestSerializer(data=request.data)
		serializer.is_valid(raise_exception=True)
		email = serializer.validated_data['email']

		# generate 6-digit code
		code = f"{random.randint(0, 999999):06d}"
		expires_at = timezone.now() + timedelta(minutes=10)

		otp = EmailOTP.objects.create(email=email, code=code, expires_at=expires_at)

		# send email (console backend by default in dev)
		subject = "Your AGHAMazingQuest login code"
		message = f"Your login code is: {code}. It expires in 10 minutes."
		from_email = getattr(settings, 'DEFAULT_FROM_EMAIL', None)
		try:
			send_mail(subject, message, from_email, [email], fail_silently=False)
		except Exception:
			# don't leak send errors to client - log and return generic response
			# but for now, surface error
			return Response({"detail": "Failed to send email."}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

		return Response({"detail": "OTP sent if the email exists."}, status=status.HTTP_200_OK)


class OTPVerifyView(APIView):
	"""Verify an OTP and return JWT tokens (creates user if needed)."""

	permission_classes = [permissions.AllowAny]

	def post(self, request):
		serializer = OTPVerifySerializer(data=request.data)
		serializer.is_valid(raise_exception=True)
		email = serializer.validated_data['email']
		code = serializer.validated_data['code']

		# find valid OTP
		otps = EmailOTP.objects.filter(email=email, code=code, used=False).order_by('-created_at')
		if not otps.exists():
			return Response({"detail": "Invalid code."}, status=status.HTTP_400_BAD_REQUEST)

		otp = otps.first()
		if not otp.is_valid():
			return Response({"detail": "Code expired or already used."}, status=status.HTTP_400_BAD_REQUEST)

		# mark used
		otp.mark_used()

		# get or create user
		username = email.split('@')[0]
		user, created = User.objects.get_or_create(email=email, defaults={'username': username})

		# issue JWT tokens using simplejwt
		from rest_framework_simplejwt.tokens import RefreshToken
		refresh = RefreshToken.for_user(user)
		return Response({"access": str(refresh.access_token), "refresh": str(refresh)})


class PasswordResetRequestView(APIView):
	"""Request a password reset email for the given email address.

	POST {"email": "user@example.com"}
	Returns 200 with a generic success message.
	"""

	permission_classes = [permissions.AllowAny]

	def post(self, request):
		form = PasswordResetForm(data=request.data)
		if form.is_valid():
			# use Django's form.save to send email using the configured EMAIL_BACKEND
			form.save(
				request=request,
				use_https=request.is_secure(),
				email_template_name='registration/password_reset_email.html',
			)
			return Response({"detail": "Password reset e-mail has been sent if the address exists."}, status=status.HTTP_200_OK)
		return Response(form.errors, status=status.HTTP_400_BAD_REQUEST)


class PasswordResetConfirmView(APIView):
	"""Confirm a password reset using uid and token (API-friendly).

	POST {"uid": "<uidb64>", "token": "<token>", "new_password1": "..", "new_password2": ".."}
	"""

	permission_classes = [permissions.AllowAny]

	def post(self, request):
		uidb64 = request.data.get('uid') or request.data.get('uidb64')
		token = request.data.get('token')
		new_password1 = request.data.get('new_password1')
		new_password2 = request.data.get('new_password2')

		if not uidb64 or not token:
			return Response({"detail": "Missing uid or token."}, status=status.HTTP_400_BAD_REQUEST)

		try:
			uid = force_str(urlsafe_base64_decode(uidb64))
			user = User.objects.get(pk=uid)
		except Exception:
			return Response({"detail": "Invalid uid."}, status=status.HTTP_400_BAD_REQUEST)

		if not default_token_generator.check_token(user, token):
			return Response({"detail": "Invalid or expired token."}, status=status.HTTP_400_BAD_REQUEST)

		form = SetPasswordForm(user, data={"new_password1": new_password1, "new_password2": new_password2})
		if form.is_valid():
			form.save()
			return Response({"detail": "Password has been reset."}, status=status.HTTP_200_OK)
		return Response(form.errors, status=status.HTTP_400_BAD_REQUEST)
