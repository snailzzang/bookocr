import os

from django.test import TestCase
from django.test import Client

from django.core.urlresolvers import resolve,reverse
from django.contrib.auth.models import AnonymousUser, User
from social.apps.django_app.default.models import UserSocialAuth

from bookshot.models import Quote, Book


def create_user(username='jhk', email='jh@gggmail.com', password='jhpassword', **kwargs):
	user = User.objects.create_user(username=username, email=email, password=password, **kwargs)
	UserSocialAuth.objects.create(user=user)
	return user


class HomeTestCase(TestCase):

	def test_root_path_exists(self):
		# Issue a GET request.
		response = self.client.get('/')
		
		# Check that the response is not 404
		self.assertNotEqual(response.status_code, 404)

	def test_unlogged_in_user_gets_redirected_to_login(self):
		response = self.client.get('/')
		
		self.assertEqual(response.status_code, 302)
		self.assertTrue(response.url.startswith('/login'))

	def test_logged_in_user_gets_a_welcome(self):
		user = create_user()
		self.client.force_login(user)

		#
		response = self.client.get('/')
		self.assertEqual(response.status_code, 200)
