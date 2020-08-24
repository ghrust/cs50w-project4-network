from django.test import TestCase, Client

# Create your tests here.
class NetworkTestCase(TestCase):
    """Tests for Network app."""

    def test_index_page(self):
        """Test index page."""

        c = Client()
        response = c.get('/')

        self.assertEqual(response.status_code, 200)
