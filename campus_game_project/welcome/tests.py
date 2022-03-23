from django.test import Client, TestCase
from welcome.models import User


class UserTestCase(TestCase):

    def setUp(self):
        User.objects.create(name="TestUser", email="test@exeter.ac.uk", password="password")
        User.objects.create(name="TestUser2", email="test2@exeter.ac.uk", password="password")

    def test_user_creation(self):
        user = User.objects.filter(name="TestUser")
        self.assertEqual(len(user), 1)

    def test_user_fields(self):
        user = User.objects.get(name="TestUser")
        self.assertEqual(user.name, "TestUser")
        self.assertEqual(user.email, "test@exeter.ac.uk")
        self.assertEqual(user.password, "password")
        self.assertEqual(user.status, 1)
        self.assertEqual(user.points, 0)
        self.assertEqual(user.profile_image_url, "home/human1.png")

    def test_delete_user(self):
        user = User.objects.get(name="TestUser2")
        user.delete()
        users = User.objects.filter(name="TestUser2")
        self.assertEqual(len(users), 0)

    def test_user_update(self):
        user = User.objects.get(name="TestUser")
        user.points = 1000
        user.save()
        new_user = User.objects.get(name="TestUser")
        self.assertEqual(new_user.points, 1000)


class WelcomeTestCase(TestCase):

    def setUp(self):
        self.client = Client()

    def test_welcome_response_code(self):
        response = self.client.get('')
        self.assertEqual(response.status_code, 200)


class SignupTestCase(TestCase):

    def setUp(self):
        self.client = Client()

    def test_signup_response_code(self):
        response = self.client.get('/signup/')
        self.assertEqual(response.status_code, 200)


class SigninTestCase(TestCase):

    def setUp(self):
        self.client = Client()

    def test_signin_response_code(self):
        response = self.client.get('/signin/')
        self.assertEqual(response.status_code, 200)


class LegalTestCase(TestCase):

    def setUp(self):
        self.client = Client()

    def test_legal_response_code(self):
        response = self.client.get('/legal/')
        self.assertEqual(response.status_code, 200)

    def test_legal_context(self):
        response = self.client.post('/legal/', {'origin': 'test'})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['origin'], 'test')
