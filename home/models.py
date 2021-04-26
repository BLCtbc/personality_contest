from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import ugettext_lazy as _
from .managers import UserManager

# from django.contrib import postgres.fields as postgres_fields


# Create your models here.
class User(AbstractUser):
	username = None
	email = models.EmailField(_('email address'), unique=True)
	date_joined = models.DateTimeField(_('date joined'), auto_now_add=True)
	is_active = models.BooleanField(_('active'), default=True)
	notify = models.BooleanField(_('active'), default=True, help_text="Indicates whether or not the user will receive emails via mailing list")


	objects = UserManager()
	USERNAME_FIELD = 'email'
	REQUIRED_FIELDS = []

	def __str__(self):
		return "email: {}, \nnotify: {}, \nsuperuser: {}, \nstaff: {}".format(self.email, self.notify, self.is_superuser, self.is_staff)


class Show(models.Model):
	date = models.DateField()
	start = models.TimeField()
	end = models.TimeField()
	play_time = models.TimeField()
	city = models.CharField(max_length=40)
	state = models.CharField(max_length=20, help_text="State or Province")
	venue = models.CharField(max_length=50)
	# ages = postgres_fields.IntegerRangeField()

	def __str__(self):
		return "{}, from {} to {} @{} in {}".format(self.date, self.start, self.end, self.venue, self.city)
