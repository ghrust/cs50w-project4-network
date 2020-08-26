from django.test import TestCase, Client
from .models import User


class NetworkTestCase(TestCase):
    """Tests for Network app."""

    def setUp(self):
        # Create test user.
        user = User.objects.create_user(
            username='user1',
            password='pass',
            email='user1@testmail.com'
        )

    def test_index_page(self):
        """Test index page."""

        c = Client()
        response = c.get('/')

        self.assertEqual(response.status_code, 200)

    def test_get_request_login_page(self):
        """Test login page."""

        response = Client().get('/login')

        self.assertEqual(response.status_code, 200)

    def test_post_request_login_page_valid_username_and_password(self):
        """
        Test post request for login page
        if username and passowrd is valid.
        """

        response = Client().post(
            '/login',
            {'username': 'user1', 'password': 'pass'}
        )

        self.assertEqual(response.status_code, 302)

    def test_post_request_login_page_invalid_username(self):
        """Test post request for login if username is invalid."""

        response = Client().post(
            '/login',
            {'username': 'user2', 'password': 'pass'}
        )

        self.assertEqual(response.status_code, 200)

    def test_logout(self):
        """Test logout view."""

        response = Client().get('/logout')

        self.assertEqual(response.status_code, 302)
