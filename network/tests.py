from django.test import TestCase, Client
from .models import User, Post
from .forms import NewPostForm


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

        self.assertRedirects(response, '/')

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

        self.assertRedirects(response, '/')

    def test_get_request_register_page(self):
        """Test register page."""

        response = Client().get('/register')

        self.assertEqual(response.status_code, 200)

    def test_valid_registration(self):
        """Test registration with valid username, password and email."""

        response = Client().post(
            '/register',
            {
                'username': 'user2',
                'password': 'pass',
                'confirmation': 'pass',
                'email': 'user2@testmail.com'
            }
        )

        user = User.objects.get(username='user2')

        self.assertRedirects(response, '/')
        self.assertEqual(user.username, 'user2')
        self.assertEqual(user.email, 'user2@testmail.com')

    def test_invalid_registration_with_wrong_password_confirmation(self):
        """Test invalid registration with wrong password confirmation."""

        response = Client().post(
            '/register',
            {
                'username': 'user2',
                'password': 'pass',
                'confirmation': 'paas',
                'email': 'user2@testmail.com'
            }
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context["message"], "Passwords must match.")

    def test_invalid_registration_if_name_already_taken(self):
        """Test invalid registration if name already taken."""

        response = Client().post(
            '/register',
            {
                'username': 'user1',
                'password': 'pass',
                'confirmation': 'pass',
                'email': 'user2@testmail.com'
            }
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response.context["message"],
            "Username already taken."
        )

    def test_new_post_form_rendered(self):
        """Test create post."""

        response = Client().get('/')

        form = NewPostForm()

        self.assertContains(response, form)

    def test_get_request_new_post(self):
        """Test get request to new post view."""

        response = Client().get('/new_post')

        self.assertRedirects(response, '/')

    def test_add_new_post(self):
        """Test new post view. Post request to server. Save to database."""

        c = Client()
        c.login(username='user1', password='pass')

        response = c.post(
            '/new_post',
            {'post': 'test'}
        )

        c.logout()

        posts = Post.objects.all()

        self.assertRedirects(response, '/')
        self.assertEqual(posts.count(), 1)
