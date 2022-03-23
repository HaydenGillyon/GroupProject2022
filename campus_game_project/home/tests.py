from django.test import Client, TestCase
from welcome.models import User


def set_login(client, email):
    session = client.session
    session['login'] = True
    session['email'] = email
    session.save()


class HomeTestCase(TestCase):

    def setUp(self):
        User.objects.create(name="RoryHome", email="rc680home@exeter.ac.uk", password="password")
        self.client = Client()
        set_login(self.client, "rc680home@exeter.ac.uk")
    
    def test_home_response_code(self):
        response = self.client.get('/home/')
        self.assertEqual(response.status_code, 200)

    def test_home_redirect(self):
        self.client.session.flush()
        response = self.client.get('/home/')
        self.assertEqual(response.status_code, 302)
        set_login(self.client, "rc680home@exeter.ac.uk")

    def test_home_context(self):
        response = self.client.get('/home/')
        self.assertEqual(response.context['user'], "RoryHome")
        self.assertEqual(response.context['email'], "rc680home@exeter.ac.uk")
        self.assertEqual(response.context['id'], 1)


class ProfileTestCase(TestCase):

    def setUp(self):
        User.objects.create(name="RoryProfile", email="rc680profile@exeter.ac.uk", password="password")
        self.client = Client()
        set_login(self.client, "rc680profile@exeter.ac.uk")

    def test_profile_response_code(self):
        response = self.client.get('/home/profile/')
        self.assertEqual(response.status_code, 200)

    def test_profile_redirect(self):
        self.client.session.flush()
        response = self.client.get('/home/profile/')
        self.assertEqual(response.status_code, 302)
        set_login(self.client, "rc680profile@exeter.ac.uk")

    def test_profile_context(self):
        response = self.client.get('/home/profile/')
        self.assertEqual(response.context['user'], "RoryProfile")
        self.assertEqual(response.context['email'], "rc680profile@exeter.ac.uk")
        self.assertEqual(response.context['id'], 1)
        self.assertEqual(response.context['points'], 0)
        self.assertEqual(response.context['profile'], "home/human1.png")

    def test_profile_post(self):
        response = self.client.post('/home/profile/', {'profile_pic': 'test'})
        self.assertEqual(response.context['profile'], "test")


class LeaderboardTestCase(TestCase):

    def setUp(self):
        User.objects.create(name="RoryLeaderboard", email="rc680leaderboard@exeter.ac.uk", password="password")
        self.client = Client()
        set_login(self.client, "rc680leaderboard@exeter.ac.uk")

    def test_leaderboard_response_code(self):
        response = self.client.get('/home/leaderboard/')
        self.assertEqual(response.status_code, 200)

    def test_leaderboard_redirect(self):
        self.client.session.flush()
        response = self.client.get('/home/leaderboard/')
        self.assertEqual(response.status_code, 302)
        set_login(self.client, "rc680leaderboard@exeter.ac.uk")

    def test_leaderboard_context(self):
        response = self.client.get('/home/leaderboard/')
        self.assertEqual(len(response.context['data']), 1)
        self.assertEqual(response.context['data'].first().name, "RoryLeaderboard")


class LogoutTestCase(TestCase):

    def setUp(self):
        self.client = Client()

    def test_logout_response_code(self):
        response = self.client.get('/home/logout/')
        self.assertEqual(response.status_code, 302)

    def test_logout_functionality(self):
        session = self.client.session
        session['test'] = True
        session.save()
        self.assertEqual('test' in self.client.session, True)
        self.client.get('/home/logout/')
        self.assertEqual('test' in self.client.session, False)
