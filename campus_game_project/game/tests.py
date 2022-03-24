from attr import validate
from django.test import Client, TestCase
from game.models import Game, Player
from game.views import *
from welcome.models import User


def set_login(client):
    session = client.session
    session['login'] = True
    session.save()


class GameTestCase(TestCase):

    def setUp(self):
        game = Game.objects.create(lobby_code=1111, player_num=1)
        user = User.objects.create(name="Rory", email="rc680@exeter.ac.uk", password="password")
        Player.objects.create(username="Rory", game=game, user=user, seeker=False, ready=False)

    def test_game_creation(self):
        game = Game.objects.filter(lobby_code=1111)
        self.assertEqual(len(game), 1)

    def test_game_fields(self):
        game = Game.objects.get(lobby_code=1111)
        self.assertEqual(game.lobby_code, 1111)
        self.assertEqual(game.player_num, 1)
        self.assertEqual(game.players_finished, 0)
        self.assertEqual(game.game_start_time, 0)
        self.assertEqual(game.running, False)
        self.assertEqual(game.winner, 'N')
        self.assertEqual(game.hiding_time, 60)
        self.assertEqual(game.seeking_time, 600)
        self.assertEqual(game.seeker_num, 1)
        self.assertEqual(game.radius, 100)
        self.assertEqual(game.lobby_longitude, 0.0)
        self.assertEqual(game.lobby_latitude, 0.0)

    def test_game_update(self):
        game = Game.objects.get(lobby_code=1111)
        game.hiding_time = 70
        game.save()
        new_game = Game.objects.get(lobby_code=1111)
        self.assertEqual(new_game.hiding_time, 70)

    def test_all_ready(self):
        game = Game.objects.get(lobby_code=1111)
        self.assertEqual(game.all_ready(), False)
        player = Player.objects.get(username="Rory")
        player.ready = True
        player.save()
        self.assertEqual(game.all_ready(), True)

    def test_game_delete(self):
        game = Game.objects.get(lobby_code=1111)
        game.delete()
        self.assertEqual(len(Game.objects.all()), 0)


class PlayerTestCase(TestCase):

    def setUp(self):
        game = Game.objects.create(lobby_code=1111, player_num=1)
        user = User.objects.create(name="Rory", email="rc680@exeter.ac.uk", password="password")
        Player.objects.create(username="Rory", game=game, user=user, seeker=False, ready=False)

    def test_player_creation(self):
        player = Player.objects.filter(username="Rory")
        self.assertEqual(len(player), 1)

    def test_player_fields(self):
        player = Player.objects.get(username="Rory")
        game = Game.objects.get(lobby_code=1111)
        user = User.objects.get(name="Rory")
        self.assertEqual(player.username, "Rory")
        self.assertEqual(player.game, game)
        self.assertEqual(player.user, user)
        self.assertEqual(player.seeker, False)
        self.assertEqual(player.ready, False)
        self.assertEqual(player.hider_code, None)
        self.assertEqual(player.found, False)
        
    def test_player_update(self):
        player = Player.objects.get(username="Rory")
        player.ready = True
        player.save()
        new_player = Player.objects.get(username="Rory")
        self.assertEqual(new_player.ready, True)

    def test_player_delete(self):
        player = Player.objects.get(username="Rory")
        player.delete()
        self.assertEqual(len(Player.objects.all()), 0)


class CreateTestCase(TestCase):

    def setUp(self):
        self.client = Client()
        set_login(self.client)

    def test_create_response_code(self):
        response = self.client.get('/game/create/')
        self.assertEqual(response.status_code, 200)

    def test_create_redirect(self):
        self.client.session.flush()
        response = self.client.get('/game/create/')
        self.assertEqual(response.status_code, 302)
        set_login(self.client)

    def test_create_context(self):
        response = self.client.get('/game/create/')
        self.assertEqual('lobby_code' in response.context, True)


class JoinTestCase(TestCase):

    def setUp(self):
        self.client = Client()
        set_login(self.client)

    def test_join_response_code(self):
        response = self.client.get('/game/join/')
        self.assertEqual(response.status_code, 200)

    def test_join_redirect(self):
        self.client.session.flush()
        response = self.client.get('/game/join/')
        self.assertEqual(response.status_code, 302)


class CodeTestCase(TestCase):

    def test_code_is_number(self):
        code = generate_code()
        self.assertEqual(int(code), code)

    def test_code_range(self):
        code = generate_code()
        self.assertEqual(1000 <= code < 10000, True)


class InputsTestCase(TestCase):

    def test_null_inputs(self):
        post = {
            'hiding_time': '',
            'seeking_time': '',
            'seeker_num': '',
            'radius': ''
        }

        self.assertEqual(validate_inputs(post)[0], True)

    def test_letter_inputs(self):
        post = {
            'hiding_time': 'a',
            'seeking_time': 'b',
            'seeker_num': 'c',
            'radius': 'd'
        }

        results = validate_inputs(post)

        self.assertEqual(results[0], False)
        self.assertEqual(results[1], "Settings must be digits!")

    def test_bad_hiding_time(self):
        post = {
            'hiding_time': '1',
            'seeking_time': '',
            'seeker_num': '',
            'radius': ''
        }
        
        results = validate_inputs(post)

        self.assertEqual(results[0], False)
        self.assertEqual(results[1], "Hiding time must be between 20 and 120 seconds!")

    def test_bad_seeking_time(self):
        post = {
            'hiding_time': '',
            'seeking_time': '1',
            'seeker_num': '',
            'radius': ''
        }
        
        results = validate_inputs(post)

        self.assertEqual(results[0], False)
        self.assertEqual(results[1], "Seeking time must be between 120 and 1200 seconds!")

    def test_bad_seeker_num(self):
        post = {
            'hiding_time': '',
            'seeking_time': '',
            'seeker_num': '0',
            'radius': ''
        }
        
        results = validate_inputs(post)

        self.assertEqual(results[0], False)
        self.assertEqual(results[1], "Seekers must be between 1 and 8!")

    def test_bad_radius(self):
        post = {
            'hiding_time': '',
            'seeking_time': '',
            'seeker_num': '',
            'radius': '1'
        }
        
        results = validate_inputs(post)

        self.assertEqual(results[0], False)
        self.assertEqual(results[1], "Radius must be between 50 and 1000 meters!")

    def test_valid(self):
        post = {
            'hiding_time': '100',
            'seeking_time': '600',
            'seeker_num': '1',
            'radius': '100'
        }
        
        results = validate_inputs(post)

        self.assertEqual(results[0], True)


class CreateGameTestCase(TestCase):

    def test_null_inputs(self):
        post = {
            'hiding_time': '',
            'seeking_time': '',
            'seeker_num': '',
            'radius': '',
            'lobby_latitude': 0,
            'lobby_longitude': 0
        }

        results = create_game(post, 1111)

        self.assertEqual(results[0], True)
        self.assertEqual(len(Game.objects.all()), 1)

    def test_bad_inputs(self):
        post = {
            'hiding_time': 'a',
            'seeking_time': 'b',
            'seeker_num': 'c',
            'radius': 'd'
        }

        results = create_game(post, 1111)

        self.assertEqual(results[0], False)
        self.assertEqual(results[1], "Settings must be digits!")
        self.assertEqual(len(Game.objects.all()), 0)

    def test_good_inputs(self):
        post = {
            'hiding_time': '100',
            'seeking_time': '600',
            'seeker_num': '1',
            'radius': '100',
            'lobby_latitude': 0,
            'lobby_longitude': 0
        }

        results = create_game(post, 1111)

        self.assertEqual(results[0], True)
        self.assertEqual(len(Game.objects.all()), 1)


class CreatePlayerTestCase(TestCase):

    def setUp(self):
        game = Game.objects.create(lobby_code=1111, player_num=1)
        user = User.objects.create(name="Rory", email="rc680@exeter.ac.uk", password="password")
        User.objects.create(name="Rory2", email="rc6802@exeter.ac.uk", password="password")
        Player.objects.create(username="Rory", game=game, user=user, seeker=False, ready=False)

    def test_duplicate_username(self):
        game = Game.objects.get(lobby_code=1111)
        result = create_player(game, "Rory", "rc6802@exeter.ac.uk")
        self.assertEqual(result, False)
        self.assertEqual(len(Player.objects.all()), 1)

    def test_valid(self):
        game = Game.objects.get(lobby_code=1111)
        result = create_player(game, "Rory2", "rc6802@exeter.ac.uk")
        self.assertEqual(result, True)
        self.assertEqual(len(Player.objects.all()), 2)


class CheckRejoinTestCase(TestCase):

    def setUp(self):
        game = Game.objects.create(lobby_code=1111, player_num=1)
        user = User.objects.create(name="Rory", email="rc680@exeter.ac.uk", password="password")
        Player.objects.create(username="Rory", game=game, user=user, seeker=False, ready=False)

    def check_valid(self):
        game = Game.objects.get(lobby_code=1111)
        result = check_rejoin(game, "rc680@exeter.ac.uk")
        self.assertEqual(result, True)

    def check_invalid(self):
        game = Game.objects.get(lobby_code=1111)
        result = check_rejoin(game, "test")
        self.assertEqual(result, False)
