from unittest import TestCase
from django.test import Client
from book_sender.models import Category


class HomeTestCase(TestCase):

    def test_health_check(self):
        c = Client()
        response = c.get("/")
        self.assertEqual(response.status_code, 200)
        
