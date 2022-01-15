from django.test import TestCase
from django.contrib.auth.models import User

# Create your tests here.
from django.test import SimpleTestCase
from django.urls import reverse
from django.test.client import Client
import unittest


class LoginTestCase(unittest.TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user('john', 'lennon@thebeatles.com', 'johnpassword')

    def testLoginPosts(self):
        self.client.login(username='john', password='johnpassword')
        response = self.client.get(reverse('all_posts'))
        self.assertEqual(response.status_code, 200)
        response = self.client.get(reverse('index'))
        self.assertEqual(response.status_code, 200)
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        response = self.client.get(reverse('all_posts'))
        self.assertEqual(response.status_code, 200)
        response = self.client.get('/post/')
        self.assertEqual(response.status_code, 200)
        response = self.client.get('/post/posts/')
        self.assertEqual(response.status_code, 200)
        response = self.client.get('/post/newpost/')
        self.assertEqual(response.status_code, 200)
        response = self.client.get('/user/profile/{0}'.format(self.user.id))
        self.assertEqual(response.status_code, 200)

class LoginOutTestCase(SimpleTestCase):
    def test_homepage_status_code(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 302)
        response = self.client.get(reverse('index'))
        self.assertEqual(response.status_code, 302)
        response = self.client.get('/post/')
        self.assertEqual(response.status_code, 302)
        response = self.client.get(reverse('all_posts'))
        self.assertEqual(response.status_code, 302)

