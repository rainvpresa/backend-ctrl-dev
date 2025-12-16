from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
	"""Custom user model for AGHAMazingQuest mobile backend.

	Stores basic profile info and a simple `scores` field for tracking user points.
	"""

	scores = models.IntegerField(default=0)

	# Public display name used across the UI (optional, falls back to username)
	display_name = models.CharField(max_length=150, blank=True)

	# Avatar image (stored under MEDIA_ROOT). Requires Pillow.
	avatar = models.ImageField(upload_to='avatars/', null=True, blank=True)
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)

	def __str__(self):
		return self.username


class EmailOTP(models.Model):
	email = models.EmailField()
	code = models.CharField(max_length=10)
	created_at = models.DateTimeField(auto_now_add=True)
	expires_at = models.DateTimeField()
	used = models.BooleanField(default=False)

	class Meta:
		indexes = [models.Index(fields=["email", "code"])]

	def is_valid(self):
		from django.utils import timezone
		return (not self.used) and timezone.now() < self.expires_at

	def mark_used(self):
		self.used = True
		self.save(update_fields=["used"]) 
