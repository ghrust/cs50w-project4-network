from django.test import TestCase, Client
from .models import User, Post, UserFollowing
from .forms import NewPostForm


class NetworkTestCase(TestCase):
    """Tests for Network app."""

    def setUp(self):
        # Create test user.
        user1 = User.objects.create_user(
            username='user1',
            password='pass',
            email='user1@testmail.com',
        )

        User.objects.create_user(
            username='user2',
            password='pass',
            email='user2@testmail.com',
        )

        Post.objects.create(
            content='test',
            author=user1,
        )

    def test_index_page(self):
        """Test index page."""

        c = Client()
        response = c.get('/')

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['posts'].count(), 1)

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
            {'username': 'user3', 'password': 'pass'}
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
                'username': 'user3',
                'password': 'pass',
                'confirmation': 'pass',
                'email': 'user3@testmail.com'
            }
        )

        user = User.objects.get(username='user3')

        self.assertRedirects(response, '/')
        self.assertEqual(user.username, 'user3')
        self.assertEqual(user.email, 'user3@testmail.com')

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

        self.assertIsInstance(response.context['form'], NewPostForm)

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
        self.assertEqual(posts.count(), 2)

    def test_profile_page(self):
        """Test user profile page."""

        c = Client()
        c.login(username='user1', password='pass')

        posts = Post.objects.filter(author=User.objects.get(username='user1'))

        response = c.get('/profile/user1')

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['username'], 'user1')
        self.assertEqual(response.context['posts'].count(), posts.count())

    def test_follow(self):
        """Test user follow another user."""

        c = Client()
        c.login(username='user1', password='pass')
        c.get('/follow/user2')
        response = c.get('/profile/user2')

        self.assertEqual(response.context['followers'].count(), 1)

        UserFollowing.objects.get(follower=1, following=2).delete()

    def test_unfollow(self):
        """Test unfollow."""

        user1 = User.objects.get(pk=1)
        user2 = User.objects.get(pk=2)
        UserFollowing.objects.create(follower=user1, following=user2)

        c = Client()
        c.login(username='user1', password='pass')
        c.get('/unfollow/user2')
        response = c.get('/profile/user2')

        self.assertEqual(response.context['followers'].count(), 0)

    def test_following_posts_page(self):
        """Test following posts page."""

        c = Client()
        c.login(username='user2', password='pass')
        c.get('/follow/user1')

        response = c.get('/following_posts')

        self.assertEqual(response.context['f_posts'].count(), 1)

    def test_following_posts_page_unauthorized_user(self):
        """Test page with following posts if user is unauthorized."""

        c = Client()
        response = c.get('/following_posts')

        self.assertRedirects(response, '/')

    def test_edit_post_view_get(self):
        """Test edit post view. GET."""

        c = Client()
        response = c.get('/edit_post')

        self.assertRedirects(response, '/')

    def test_edit_post_view_post(self):
        """Test edit post view. POST."""

        c = Client()
        c.login(username='user1', password='pass')

        response = c.post(
            '/edit_post',
            {'post_id': '1', 'edited_text': 'test'},
            content_type='application/json',
        )

        post = Post.objects.get(pk=1)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(post.content, 'test')
